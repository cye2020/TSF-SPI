# 전산업지수


from PublicDataReader import Kosis
import pandas as pd




# KOSIS 공유서비스 Open API 사용자 인증키
keys = pd.read_csv('Key.csv', index_col=0)
kosis_service_key = keys.loc['Kosis', 'Key']

# 인스턴스 생성하기
kosis_api = Kosis(kosis_service_key)

df1 = kosis_api.get_data(
    "KOSIS통합검색",
    searchNm="전산업생산지수",
    )

pd.set_option('display.max_columns', None)
print(df1.head(1))

tblId = 'DT_1JH20201'
orgId = "101"

df2 = kosis_api.get_data(
    "통계표설명",
    "분류항목",
    orgId = orgId,
    tblId = tblId,
    )
print(df2.head(1))
df2.to_csv('test.csv')
print('------------------------------------------------------')

df5 = kosis_api.get_data(
    "통계자료",
    orgId = orgId,
    tblId = tblId,
    itmId = "ALL",
    objL1 = "ALL",
    prdSe = "M",
    startPrdDe='20000101',
    endPrdDe='2024',
    )

print(df5)