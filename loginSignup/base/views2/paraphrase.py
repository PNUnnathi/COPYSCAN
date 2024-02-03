from django.shortcuts import render
from django.views import View

import warnings

warnings.filterwarnings("ignore")


class ParaphraseTextView(View):
    template_name = 'paraphrase.html'

    def get(self, request):
        # Retrieve the original text from the session
        input_text = request.session.get('paraphrase_input_text')

        # Perform paraphrasing logic using the Parrot paraphraser
        if input_text:
            try:
                parrot = self.init_parrot()
                paraphrased_texts = parrot.augment(input_phrase=input_text)
                paraphrased_text = '\n'.join(paraphrased_texts)
            except Exception as e:
                # Handle any exceptions that might occur during paraphrasing
                print(f"Error during paraphrasing: {e}")
                paraphrased_text = "Error during paraphrasing"
        else:
            print("No input text available")
            paraphrased_text = "No input text available"

        return render(request, self.template_name, {'input_text': input_text, 'paraphrased_text': paraphrased_text})
