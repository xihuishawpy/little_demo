# https://facebook.github.io/prophet/docs/quick_start.html#python-api

from prophet import Prophet
import pandas as pd

df = pd.read_csv('example_wp_log_peyton_manning.csv')

# 0、基本方法
# 创建预测器，拟合数据
m = Prophet()
m.fit(df)

# 设置预测框
future = m.make_future_dataframe(periods=365)
future.tail()

# 对未来时间点进行预测，预测给出预测值和置信区间
forecast = m.predict(future)
forecast[['ds','yhat','yhat_lower','yhat_upper']].tail()

# 画图
fig1 = m.plot(forecast)
# 画出分量图
fig2 = m.plot_components(forecast)


# 1、对【假期和特别活动】进行建模
# 通过 holidays 参数，将假期因素加入模型
playoffs = pd.DataFrame({
  'holiday': 'playoff',
  'ds': pd.to_datetime(['2008-01-13', '2009-01-03', '2010-01-16',
                        '2010-01-24', '2010-02-07', '2011-01-08',
                        '2013-01-12', '2014-01-12', '2014-01-19',
                        '2014-02-02', '2015-01-11', '2016-01-17',
                        '2016-01-24', '2016-02-07']),
  'lower_window': 0,
  'upper_window': 1,
})
superbowls = pd.DataFrame({
  'holiday': 'superbowl',
  'ds': pd.to_datetime(['2010-02-07', '2014-02-02', '2016-02-07']),
  'lower_window': 0,
  'upper_window': 1,
})
holidays = pd.concat((playoffs, superbowls))

# 传入假期时间构建预测器
m = Prophet(holidays=holidays)
forecast = m.fit(df).predict(future)
fig = m.plot_components(forecast)


# 2、另外引入【法定节假日】，加入模型（通过add_country_holidays方法）
m = Prophet(holidays=holidays)
m.add_country_holidays(country_name='US') # CN ：中国法定节假日
m.fit(df)

forecast = m.predict(future)
fig = m.plot_components(forecast)


# 3、季节性的傅里叶顺序
# 使用“部分傅里叶和"来估计季节性
# 年季节性，默认是10；周季节性，默认是3
# 增加傅立叶项的数量可以使季节性适应更快的变化周期，但也可能导致过度拟合
from prophet.plot import plot_yearly
m = Prophet(yearly_seasonality=20).fit(df)
a = plot_yearly(m)


# 4、指定自定义季节性
# Prophet默认：【每周】和【每年】的季节性，可以使用 add_seasonality方法添加其他季节性，比如每月、每季度、每小时
# 关闭周季节性，加入月季节性
m = Prophet(weekly_seasonality=False)
m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
forecast = m.fit(df).predict(future)
fig = m.plot_components(forecast)


# 5、其他因素影响的季节性
# 比如旺季、淡季的周季节性不同

# 划分淡旺季月份
def is_nfl_season(ds):
    date = pd.to_datetime(ds)
    return (date.month > 8 or date.month < 2)

df['on_season'] = df['ds'].apply(is_nfl_season)
df['off_season'] = ~df['ds'].apply(is_nfl_season)

# 把默认的周季节性关闭，加入自定义的周季节性（淡旺季）
m = Prophet(weekly_seasonality=False)
m.add_seasonality(name='weekly_on_season', period=7, fourier_order=3, condition_name='on_season')
m.add_seasonality(name='weekly_off_season', period=7, fourier_order=3, condition_name='off_season')

# 同时，也要标注未来日期
future['on_season'] = future['ds'].apply(is_nfl_season)
future['off_season'] = ~future['ds'].apply(is_nfl_season)

forecast = m.fit(df).predict(future)
fig = m.plot_components(forecast)


# 如果发现假期效应过拟合了，可以通过holidays_prior_scale参数调整，默认是10
# para: holidays_prior_scale，降低该参数会减弱假期效应；seasonality_prior_scale，季节效应同理 ，
m = Prophet(holidays=holidays, holidays_prior_scale=0.05).fit(df)
forecast = m.predict(future)
forecast[(forecast['playoff'] + forecast['superbowl']).abs() > 0][
    ['ds', 'playoff', 'superbowl']][-10:]


# 6、增加其他回归因子
def nfl_sunday(ds):
    date = pd.to_datetime(ds)
    return 1 if date.weekday() == 6 and (date.month > 8 or date.month < 2) else 0

df['nfl_sunday'] = df['ds'].apply(nfl_sunday)

m = Prophet()
m.add_regressor('nfl_sunday')
m.fit(df)

# 未来数据帧也必须有这个因子
future['nfl_sunday'] = future['ds'].apply(nfl_sunday)

forecast = m.predict(future)
fig = m.plot_components(forecast)





