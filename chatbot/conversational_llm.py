from typing import Dict, List
from string import Template
import google.generativeai as genai
from chatbot.pizza_functions import PizzaFunctions

class ConversationalLLM:
    def __init__(self, model_config: Dict, system_prompt: str | Template = "", tools: List = []):
        self.system_prompt = system_prompt
        self.model_config = model_config
        self.conversation_history = []
        self.tools = tools
        self.client = None

    def _create_client(self, system_prompt: str):
        if self.client is None:
            self.client = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=self.model_config,
                system_instruction=system_prompt,
                tools=self.tools
            ).start_chat()
        return self.client

    def modify_system_prompt(self, **kwargs) -> str:
        return self.system_prompt.substitute(**kwargs) if isinstance(self.system_prompt, Template) else self.system_prompt

    def limit_conversation_history(self) -> None:
        n_history = self.model_config.get("n_history", 5)
        if len(self.conversation_history) / 2 > n_history:
            del self.conversation_history[:2]

    def get_response(self, user_input: str, **kwargs) -> str:
        system_prompt = self.modify_system_prompt(**kwargs)

        if len(system_prompt) < 10000 and len(user_input) < 1000:
            client = self._create_client(system_prompt)
            response = client.send_message(user_input)
            complete_response = ""  # Accumulate the full response

            for part in response.parts:
                print(part)
                if "function_call" in part:
                    function_name = part.function_call.name
                    try:
                        if function_name == "get_menu":
                            result = PizzaFunctions.get_menu(**part.function_call.args)
                        elif function_name == "insert_order":
                            result = PizzaFunctions.insert_order(**part.function_call.args)
                        elif function_name == "finalize_orders":
                            result = PizzaFunctions.finalize_orders(**part.function_call.args)
                        else:
                            result = f"Unknown function: {function_name}"

                        # TODO: observe how the function response is sent to the LLM
                        function_response = genai.protos.FunctionResponse(
                            name=function_name,
                            response={'result': result}
                        )
                        response = client.send_message(
                            genai.protos.Content(
                                parts=[genai.protos.Part(function_response=function_response)]
                            )
                        )
                        complete_response += response.text # Append function response

                    except Exception as e: # Catch and handle errors
                        complete_response += f"Error executing {function_name}: {e}"
                        function_response = genai.protos.FunctionResponse(
                            name=function_name,
                            response={'result': f"Error: {e}"}
                        )
                        response = client.send_message(
                            genai.protos.Content(
                                parts=[genai.protos.Part(function_response=function_response)]
                            )
                        )
                else:
                    complete_response += part.text


            self.conversation_history.extend([
                {"role": "user", "parts": [user_input]},
                {"role": "model", "parts": [complete_response]} # Store complete response
            ])
            self.limit_conversation_history()
            return complete_response

        else:
            return "Token terlalu panjang"
