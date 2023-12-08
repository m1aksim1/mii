import os.path
import random

from flask import Flask, redirect, url_for, request, render_template
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier




import BloomFilter
import functions
from DecisionTree import DecisionTree

app = Flask(__name__)


@app.route("/")
def home():
    return open("main.html", 'r', encoding='utf-8').read()


@app.route("/get_table", methods=['GET', 'POST'])
def get_table():
    data = request.args
    start_row: int = int(data['start_row'])
    end_row: int = int(data['end_row'])
    start_column: int = int(data['start_column'])
    end_column: int = int(data['end_column'])
    # print(csv_to_html_table("Diamonds Prices2022.csv", start_row, end_row, start_column, end_column));
    return functions.csv_to_html_table("Diamonds Prices2022.csv", start_row, end_row, start_column, end_column)


@app.route("/lab2", methods=['GET', 'POST'])
def lab2():

    #огранка
    html_table = functions.array_to_html(functions.group_by_column("Diamonds Prices2022.csv", 2))

    #караты
    my_array = functions.group_by_column("Diamonds Prices2022.csv", 1)
    html_table += functions.array_to_html(functions.sort_array(my_array, 0))

    #прозрачность
    html_table += functions.array_to_html(functions.group_by_column("Diamonds Prices2022.csv", 4))

    #цвет
    html_table += functions.array_to_html(functions.group_by_column("Diamonds Prices2022.csv", 3))

    return html_table


@app.route("/lab3", methods=['GET', 'POST'])
def lab3():
    group_data = functions.group_by_column("Diamonds Prices2022.csv",1)
    sort_group_data = functions.sort_array(group_data, 0)

    avg_carat = functions.get_avg_value("Diamonds Prices2022.csv", 1, 4)
    avg_cut = functions.get_avg_value("Diamonds Prices2022.csv",2,4)
    avg_color = functions.get_avg_value("Diamonds Prices2022.csv",3,4)
    avg_clarity = functions.get_avg_value("Diamonds Prices2022.csv", 4, 4)
    avg_depth = functions.get_avg_value("Diamonds Prices2022.csv", 5, 4)
    avg_table = functions.get_avg_value("Diamonds Prices2022.csv", 6, 4)
    avg_price = functions.get_avg_value("Diamonds Prices2022.csv", 7, 4)
    avg_x = functions.get_avg_value("Diamonds Prices2022.csv", 8, 4)
    avg_y = functions.get_avg_value("Diamonds Prices2022.csv", 9, 4)
    avg_z = functions.get_avg_value("Diamonds Prices2022.csv", 10, 4)



    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(5000 / dpi, 1000 / dpi))
    mpl.rcParams.update({'font.size': 6})

    plt.axis([0, 275, 0, 20000])

    plt.title('Карат & Стоимость')
    plt.xlabel('Карат')
    plt.ylabel('Стоимость')


    y_array = []
    x_array = []

    new_y_array = []
    new_x_array = []

    sort_group_data.pop(0)
    for element in sort_group_data:
        y_array += [element[3]]
        x_array += [element[0]]

    new_data = []

    for i in range(int(len(sort_group_data)/10)):
        new_data.append([
                         float(avg_carat[random.randint(0,4)][0]),
                         avg_cut[random.randint(0,4)][0],
                         avg_color[random.randint(0,4)][0],
                         avg_clarity[random.randint(0,4)][0],
                         avg_depth[random.randint(0,4)][0],
                         avg_table[random.randint(0,4)][0],
                         float(avg_price[random.randint(0,4)][0]),
                         avg_x[random.randint(0,4)][0],
                         avg_y[random.randint(0,4)][0],
                         avg_z[random.randint(0,4)][0]
                         ])

    new_data = functions.group_by_array_column(new_data,0)
    new_data += sort_group_data
    new_data = sorted(new_data, key=lambda x: float(x[0]))
    print(new_data)
    for element in new_data:
        new_y_array += [element[3]]
        new_x_array += [str(element[0])]

    plt.plot(x_array, y_array, color='blue', linestyle='solid', label='исходные данные')
    plt.plot(new_x_array, new_y_array, color='red', linestyle='solid', label='новые данные')



    plt.legend(loc='upper right')
    fig.savefig('static/pics/trigan.png')


    picFolder = os.path.join('static', 'pics')
    app.config['UPLOAD_FOLDER'] = picFolder
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'trigan.png')
    return render_template("lab3.html", user_image = pic1)

@app.route("/lab4", methods=['GET', 'POST'])
def lab4():
    answer = ""
    req = request.args
    data1 = pd.read_csv('Diamonds Prices2022.csv', sep=',')
    key_words = functions.get_key_words(data1)
    bf1 = BloomFilter.BloomFilter(len(key_words), 0.01)
    for i in range(len(key_words)):
        bf1.add(str(key_words[i]))
    if (bf1.check(req['word'])):
        answer += '<h1>По ключевому слову найдены обьекты в Diamonds Prices2022</h1>' + functions.get_data_search(data1, req['word'])
    else:
        answer += '<h1>По ключевому слову не найдены обьекты в Diamonds Prices2022</h1>'
    data2 = pd.read_csv('diabetes.csv', sep=',')
    key_words = functions.get_key_words(data2)
    bf2 = BloomFilter.BloomFilter(len(key_words), 0.01)
    for i in range(len(key_words)):
        bf2.add(str(key_words[i]))
    if (bf2.check(req['word'])):
        answer += '<h1>По ключевому слову найдены обьекты в diabetes</h1>'  + functions.get_data_search(data2, req['word'])
    else:
        answer += '<h1>По ключевому слову не найдены обьекты в diabetes</h1>'

    data3 = pd.read_csv('healthcare-dataset-stroke-data.csv', sep=',')
    key_words = functions.get_key_words(data3)
    bf3 = BloomFilter.BloomFilter(len(key_words), 0.01)
    for i in range(len(key_words)):
        bf3.add(str(key_words[i]))
    if (bf3.check(req['word'])):
        answer += '<h1>По ключевому слову найдены обьекты в healthcare-dataset-stroke-data</h1>' + functions.get_data_search(data3, req['word'])
    else:
        answer += '<h1>По ключевому слову не найдены обьекты в healthcare-dataset-stroke-data</h1>' \

    print(answer)
    return answer

@app.route("/lab5", methods=['GET', 'POST'])
def lab5():
    data = pd.read_csv('Diamonds Prices2022.csv')
    train, check = functions.lab5(data, 99)
    plt.scatter(train[0], train[1], label='Real price')  # реальные данные
    plt.scatter(train[0], train[2], label='Pred price')  # данные полученные с помощью парной линейной регрессии
    plt.legend(fontsize=8)
    plt.savefig("static/pics/linearRegresTrain.jpg")
    plt.close()

    # оставшиеся данные
    plt.scatter(check[0], check[1], label='Real price')  # реальные данные
    plt.scatter(check[0], check[2], label='Pred price')  # данные полученные с помощью парной линейной регрессии
    plt.legend(fontsize=8)
    plt.savefig("static/pics/linnearRegresCheck.jpg")
    plt.close()


    table = "R^2=" + str(check[3]) + pd.concat([check[0], check[1], check[2]], axis=1).to_html();

    picFolder = os.path.join('static', 'pics')
    app.config['UPLOAD_FOLDER'] = picFolder
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'linearRegresTrain.jpg')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'linnearRegresCheck.jpg')
    return render_template("lab5.html", user_image1=pic1, user_image2=pic2, table = table)

@app.route("/lab6", methods=['GET', 'POST'])
def lab6():
    date = pd.read_csv("Diamonds Prices2022.csv")
    date.head()
    x = date[['cut', 'clarity']]
    newx = x.loc[:,'cut':'clarity']
    y = date['price']
    dictClarity = {'SI2': 1,
                  'SI1': 2,
                  'VS1': 3,
                  'VS2': 4,
                  'Premium': 5,
                  'VVS2': 6,
                  'VVS1' : 7,
                  'I1' : 8,
                  'IF' : 9}
    dictCut = {'Fair': 1,
                  'Good': 2,
                  'Very Good': 3,
                  'Ideal': 4,
                  'Premium': 5}

    # Замена значений в столбце 'cut' с помощью словаря
    newx['cut'] = newx['cut'].replace(dictCut)
    newx['clarity'] = newx['clarity'].replace(dictClarity)

    x_train, x_test, y_train, y_test = train_test_split(newx, y, test_size=0.3, random_state=1)

    DT = DecisionTree(x_train, y_train)
    y_pred = DT.predict(x_test)


    df = pd.DataFrame(data=y_pred,columns=['predict'])
    x_test['predict'] = y_pred
    x_test['true_price'] = y_test

    flipped_dict = {value: key for key, value in dictCut.items()}
    x_test['cut'] = x_test['cut'].replace(flipped_dict)
    flipped_dict = {value: key for key, value in dictClarity.items()}
    x_test['clarity'] = x_test['clarity'].replace(flipped_dict)


    x_test = x_test.sort_values(by=['true_price'], key=lambda newx: x_test['true_price'])
    l = len(x_test)

    plt.plot(range(l), x_test['predict'], color='red', linestyle='solid', label='сгенерированные данные')
    plt.plot(range(l), x_test['true_price'], color='blue', linestyle='solid', label='исходные данные')
    plt.show()

    return x_test.to_html()






@app.route("/test", methods=['GET', 'POST'])
def test():
    bf1 = BloomFilter.BloomFilter(10, 0.01)
    bf1.add("hello")
    print(bf1.check("hello"))
    return


if __name__ == "__main__":
    app.run(debug=False)
