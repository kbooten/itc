from openai import OpenAI

from dotenv import load_dotenv
import os
load_dotenv()  # This will load environment variables from a .env file if present
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()


def get_llm_response(prompt,model="gpt-3.5-turbo"):
  """
  returns a string
  """
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
      {"role": "user", "content": prompt}
    ]
  )
  return completion.choices[0].message.content


def main():
  prompt = "How many letters are in this string: 'asldkfjasldkfjasdf'."
  print("Prompt:", prompt)
  print("Response:",get_llm_response(prompt))


if __name__ == '__main__':
  main()

