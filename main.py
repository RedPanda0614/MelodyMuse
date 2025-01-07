from flask import Flask, request, render_template_string, render_template
import pandas as pd
import jieba
import model  # 确保 model.py 在同一文件夹下
import search

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query', methods=['GET'])
def query():
    query_songs = []
    # if request.method == 'POST':
    query_text = request.args.get('key')
    # 使用 model.py 进行查询
    result_df = model.search_with_bm25(query_text,top_n=3)
    query_list, people_result = search.people_search(query_text)
    # 将 DataFrame 转换为字典格式
    query_songs = result_df.to_dict('records')
    print(query_songs)
    return render_template('results.html', songs=query_songs, query_list=query_list, people_res=people_result, key=query_text)


# @app.route('/')
# def index():
#     return 'Hello, world!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12345)
