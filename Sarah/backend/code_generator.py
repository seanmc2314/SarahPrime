import openai
import os

class CodeGenerator:
    def generate_feature_code(self, feature_description):
        prompt = f"""
        You are an expert Python developer. Generate Python code for a Flask application feature described as: '{feature_description}'.
        The code should be a valid Python function or endpoint that integrates with an existing Flask app.
        Return only the code, no explanations.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        code = response.choices[0].message.content
        filename = f"feature_{hash(feature_description) % 10000}.py"
        return code, filename

    def generate_program_code(self, program_description):
        prompt = f"""
        You are an expert Python developer. Generate a complete Python program for: '{program_description}'.
        The program should be a standalone script with clear functionality.
        Return only the code, no explanations.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        code = response.choices[0].message.content
        program_name = f"program_{hash(program_description) % 10000}"
        return code, program_name

    def apply_change(self, change_id):
        # For simplicity, move the change to the applied folder
        # In a real app, this would integrate the code into the app
        pass
