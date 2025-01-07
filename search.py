import pandas as pd

df = pd.read_csv('all.csv')
def people_search(query, df=df):
    keys = ['歌手', '作词', '作曲', '编曲', '制作人']
    query_list = query.split()
    # print(query_list)
    res = []
    for index, row in df.iterrows():
        queries_role = []
        for query in query_list:
            query_role = []
            for key in keys:
                if pd.notna(row[key]) and query in row[key]:
                    query_role.append(key)
            queries_role.append(query_role)
        count = 0
        for l in queries_role:
            if len(l) != 0:
                count += 1
        if count == len(queries_role):
            res.append((row['歌名'], queries_role))

    # print(res)
    for r in res:
        print("合作作品：", r[0])
        for i in range(len(r[1])):
            print(f"{query_list[i]}在作品中的角色：{r[1][i]}")

    return query_list, res
# people_search("我好想你", df)