#
import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume)로 당일시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-ETH", count = 7)

#변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.5

#target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# fee = 0.0032   #수수료
# ror(수익률), np.where(조건문, 참일때 값, 거짓일 때 값)
df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)

# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# 낙폭 Draw Down 계산(누적 최대값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD(최고낙폭) 계산
print("MDD(%): ", df['dd'].max())

print(df)

#엑셀로 출력
df.to_excel("dd.xlsx")
# open(시가)	high(고가)	low(저가)	close(종가)	volume(거래량)	range(변동폭*k)	target(매수가)	ror(수익률)	hpr(누적수익률)	dd(낙폭)
