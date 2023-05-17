    
import pandas as pd
import numpy as np

def GetData(csv1, csv2):
    
# Đọc dữ liệu từ file CSV vào DataFrame
    df = pd.read_csv(csv1,  encoding='utf-8-sig')

    # Xóa bỏ kí tự "đánh giá" trong cột "rating"

    df['count'] = df['count'].str.replace('Không có đánh giá', '0')
    df['count'] = df['count'].str.replace(' đánh giá', '')
    df['score'] = df['score'].str.replace('/5', '')
    df['count'] = df['count'].apply(lambda x: int(x))
    df['score'] = df['score'].apply(lambda x: float(x))
    df['discount'] = df['discount'].apply(lambda x : float(x.strip('%')) / 100)
    df['sale_rating'] = df['sale_rating'].str.replace('Không đủ thông tin', '0')
    df['sale_rating'] = df['sale_rating'].str.replace('Nhà bán hàng mới', '0')
    df['sale_rating'] = df['sale_rating'].apply(lambda x: float(x.strip('%')) / 100)
    df['ship_on_time'] = df['ship_on_time'].str.replace('Không đủ thông tin', '0')
    df['ship_on_time'] = df['ship_on_time'].str.replace('Nhà bán hàng mới', '0')
    df['ship_on_time'] = df['ship_on_time'].apply(lambda x: float(x.strip('%')) / 100)
    df['chat_respone'] = df['chat_respone'].str.replace('Không đủ thông tin', '0')
    df['chat_respone'] = df['chat_respone'].str.replace('Nhà bán hàng mới', '0')
    df['chat_respone'] = df['chat_respone'].apply(lambda x: float(x.strip('%')) / 100)

    # Lưu DataFrame đã được xử lý vào file CSV
    df.to_csv(csv2, index=False,  encoding='utf-8-sig')



def ClearData(csv):
    df = pd.read_csv(csv,  encoding='utf-8-sig')
    df.head()
    
    min_thresold = df['count'].quantile(0.5)
    print(min_thresold)

    df = df[df['count'] > min_thresold]
    df.to_csv(csv, index=False,  encoding='utf-8-sig')
    
def main():
    GetData('data_f.csv', 'final.csv')
    ClearData('data_final.csv')




 ######## MAIN ##############
if __name__ == '__main__':
    main()