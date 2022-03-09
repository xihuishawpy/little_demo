
from prophet import Prophet
import pandas as pd

df = pd.read_csv('example_wp_log_peyton_manning.csv')

m = Prophet()
m.fit(df)

future = m.make_future_dataframe(periods=365)
future.tail()

forecast = m.predict(future)
forecast[['ds','yhat','yhat_lower','yhat_upper']].tail()

fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)


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

m = Prophet(holidays=holidays)
forecast = m.fit(df).predict(future)

fig = m.plot_components(forecast)


# 引入法定节假日，加入模型

m = Prophet(holidays=holidays)
m.add_country_holidays(country_name='US') # CN ：中国法定节假日
m.fit(df)

forecast = m.predict(future)
fig = m.plot_components(forecast)


# 改变季节性参数，默认是10
# 增加傅立叶项的数量可以使季节性适应更快的变化周期，但也可能导致过度拟合
from prophet.plot import plot_yearly
m = Prophet(yearly_seasonality=20).fit(df)
a = plot_yearly(m)


# Prophet 默认适合每周和每年的季节性
# 关闭周季节性，加入月季节性

m = Prophet(weekly_seasonality=False)
m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
forecast = m.fit(df).predict(future)
fig = m.plot_components(forecast)


# 其他因素影响的季节性
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

future['on_season'] = future['ds'].apply(is_nfl_season)
future['off_season'] = ~future['ds'].apply(is_nfl_season)
forecast = m.fit(df).predict(future)
fig = m.plot_components(forecast)



