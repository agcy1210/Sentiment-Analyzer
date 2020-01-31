import json
import re
import nltk
import fasttext
import os.path

#filePathJson = '/Users/amanchaudhary/Downloads/Cell_Phones_and_Accessories.json'

#{"overall": 5.0, "verified": true, "reviewTime": "07 14, 2014", "reviewerID": "A25MDGOMZ2GALN", "asin": "B00005N7P0", "reviewerName": "Alvey", "reviewText": "A great read every issue.", "summary": "Five Stars", "unixReviewTime": 1405296000}

filename = "/Users/amanchaudhary/Documents/projects/sih_nlp/projects/compressed_model_ratings.ftz"
model = fasttext.load_model(filename)

def rate_review(review):
    review = review.lower()
    review = re.sub(r"([.!?,'/()])", r" \1 ", review)
    result = model.predict(review,1)
    rating = result[0][0][9:]
    return rating

def get_aspects_list(filePathJson, key, aspect):
    fileContent = open(filePathJson)
    reviews = []
    rating = 0
    tokenized_sentences = []
    count = 0
    reviewText = []
    aspect_list = aspect

    for review in fileContent:
        if(count<100000):
            try:
                reviews.append(json.loads(review))
                count = count + 1
            except:
                continue
        else:
            break

    for review in reviews:
        try:
            var = nltk.sent_tokenize(review[key])     
            for sentence in var:
                tokenized_sentences.append(sentence)
        except:
            continue
        
    for sentence in tokenized_sentences:
        for el in aspect.keys():
            if(el in sentence.lower()):
                aspect_list[el].append(sentence)

    return aspect_list

#result = get_aspects_list(filePathJson, 'reviewText', aspect={'battery': [], 'camera': [], 'screen': [], 'sound':[] })

def give_aspect_rating(aspect_list):
    aspect_rating = {}
    for keys in aspect_list.keys():
        rating = 0
        for review in aspect_list[keys]:
            if('\n' in review):
                review = ''.join(review.split('\n'))
            rating += float(rate_review(review))

        aspect_rating[keys] = round(rating /len(aspect_list[keys]), 2)

    return aspect_rating

#print(give_aspect_rating(result))





