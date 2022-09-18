from flask import Flask,render_template,request
import pickle
import numpy as np

rating_df = pickle.load(open('final_ratind.pkl','rb'))
pt = pickle.load(open('book_pivat.pkl','rb'))
books = pickle.load(open('book.pkl','rb'))
similarity_scores = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(rating_df['title'].values),
                           author=list(rating_df['author'].values),
                           image=list(rating_df['Image-URL-M'].values),
                           votes=list(rating_df['num_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recomend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['author'].values))
        item.extend(list(temp_df.drop_duplicates('title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recomend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)