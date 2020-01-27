import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st


PLOT_TYPE_TARIFF = 'tariff_type'
PLOT_TYPE_LOCATION = 'location_type'

# ========================================================================================================
# Выводит гистограмму частот для определенного параметра.
# ========================================================================================================

def show_one_double_hist(_df, hist_type, param, title, ax):
    condition1, condition2 = None, None
    legend = None
    
    if hist_type == PLOT_TYPE_TARIFF:
        condition1, condition2 = _df['tariff'] == 'smart', _df['tariff'] == 'ultra'
        legend = ['Smart mean', 'Ultra mean', 'Smart', 'Ultra']
        title += ' by tariff histogram'
    elif hist_type == PLOT_TYPE_LOCATION:
        condition1, condition2 = _df['city'] == 'Москва', _df['city'] == 'Другое'
        legend = ['Moscow mean', 'Other mean', 'Moscow', 'Other']
        title += ' by location histogram'
    else:
        raise Exception('Wrong hist type: ' + hist_type)
    
    DATA1 = _df[condition1][param]
    DATA2 = _df[condition2][param]
    
    MEAN1 = DATA1.mean()
    MEAN2 = DATA2.mean()
    
    DATA1.plot(kind='hist', ax=ax, bins=30, alpha=0.6, ec='black', color='green', density=True, title = title)
    DATA2.plot(kind='hist', ax=ax, bins=30, alpha=0.38, ec='black', color='blue', density=True)
    
    ax.axvline(x=MEAN1, linewidth=1, color='green', linestyle='--')
    ax.axvline(x=MEAN2, linewidth=1, color='blue', linestyle='--')
    
    d1_count =  legend[2] + ' count: {:.0f}\n'.format(DATA1.count())
    d1_mean =   legend[2] + ' mean: {:.0f}\n'.format(MEAN1)
    d1_median = legend[2] + ' median: {:.0f}\n'.format(DATA1.median())
    d1_std =    legend[2] + ' std: {:.0f}\n\n'.format(DATA1.std())
    d2_count =  legend[3] + ' count: {:.0f}\n'.format(DATA2.count())
    d2_mean =   legend[3] + ' mean: {:.0f}\n'.format(MEAN2)
    d2_median = legend[3] + ' median: {:.0f}\n'.format(DATA2.median())
    d2_std =    legend[3] + ' std: {:.0f}'.format(DATA2.std())
    
    info_text = d1_count + d1_mean + d1_median + d1_std + d2_count + d2_mean + d2_median + d2_std
    
    info_bbox_props = dict(boxstyle='round', facecolor='white', alpha=0.2)
    ax.text(0.98, 0.71, info_text, transform=ax.transAxes, fontsize=12, 
            verticalalignment='top', horizontalalignment='right', 
            bbox=info_bbox_props)
    
    ax.legend(legend, prop={'size':12})
    ax.set_title(title)
    
def show_double_hists(_df, param, title):
    fig = plt.figure(figsize=(16, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    show_one_double_hist(_df, PLOT_TYPE_TARIFF, param, title, ax1)
    show_one_double_hist(_df, PLOT_TYPE_LOCATION, param, title, ax2)
    
    plt.show()

# ========================================================================================================
# Выводит столбчатый график долей пользователей превышающих лимит по переданному параметру.
# ========================================================================================================

def show_one_over_the_limit_bar(_df, hist_type, ax, col_name, limit_1, limit_2, title):
    count1, count2 = None, None
    parts1, parts2 = None, None
    legend = None
    labels = ['Tariff']
    
    condition1, condition2 = (_df['tariff'] == 'smart'), (_df['tariff'] == 'ultra')
    users_over_the_limit1 = _df[condition1 & (_df[col_name] > limit_1)]
    users_over_the_limit2 = _df[condition2 & (_df[col_name] > limit_2)]
    
    if hist_type == PLOT_TYPE_TARIFF:
        legend = ['Smart', 'Ultra']
        title += ' over the limit by tariff'
        count1, count2 = _df[condition1]['user_id'].count(), _df[condition2]['user_id'].count()
        parts1 = [users_over_the_limit1['user_id'].count() / count1]
        parts2 = [users_over_the_limit2['user_id'].count() / count2]
        labels = ['Tariff']
    elif hist_type == PLOT_TYPE_LOCATION:
        loc_condition1, loc_condition2 = (_df['city'] == 'Москва'), (_df['city'] == 'Другое')
        count1, count2 = _df[loc_condition1]['user_id'].count(), _df[loc_condition2]['user_id'].count()
        legend = ['Moscow', 'Other']
        title += '  over the limit by location'
        
        msk_users_over_the_limit = (
            users_over_the_limit1.query('city == "Москва"')['user_id'].count() +
            users_over_the_limit2.query('city == "Москва"')['user_id'].count()
        )
        
        other_users_over_the_limit = (
            users_over_the_limit1.query('city == "Другое"')['user_id'].count() +
            users_over_the_limit2.query('city == "Другое"')['user_id'].count()
        )
        
        parts1 = [msk_users_over_the_limit / count1]
        parts2 = [other_users_over_the_limit / count2]
        labels = ['Location']
    else:
        raise Exception('Wrong hist type: ' + hist_type)
    
    x = np.arange(len(labels))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, parts1, label=legend[0], width = width)
    rects2 = ax.bar(x + width/2, parts2, label=legend[1], width = width)
    
    info_text = 'Total {} users: {:.0f}\nTotal {} users: {:.0f}'.format(
        legend[0], 
        count1, 
        legend[1], 
        count2)
    
    info_bbox_props = dict(boxstyle='round', facecolor='white', alpha=0.2)
    ax.text(0.98, 0.82, info_text, transform=ax.transAxes, fontsize=12, 
            verticalalignment='top', horizontalalignment='right', 
            bbox=info_bbox_props)

    
    ax.set_ylabel('Part')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_yticks(np.arange(0.0, 1.2, .2))
    ax.set_xticklabels(labels)
    ax.legend(prop={'size':12})
    
    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.annotate('{:.1%}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

def show_over_the_limit_bars(_df, col_name, limit_1, limit_2, title=''):
    fig = plt.figure(figsize=(16, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
        
    show_one_over_the_limit_bar(_df, PLOT_TYPE_TARIFF, ax1, col_name, limit_1, limit_2, title)
    show_one_over_the_limit_bar(_df, PLOT_TYPE_LOCATION, ax2, col_name, limit_1, limit_2, title)
    
    plt.show()

# ========================================================================================================
# Выводит график QQPlot переденных в нее данных.
# ========================================================================================================

def qqplots_for_smart_and_ultrs(_df, hist_type, col_name):
    condition1, condition2 = None, None
    
    if hist_type == PLOT_TYPE_TARIFF:
        condition1, condition2 = _df['tariff'] == 'smart', _df['tariff'] == 'ultra'
        tatle1, tatle2 = 'Smart', 'Ultra'
    elif hist_type == PLOT_TYPE_LOCATION:
        condition1, condition2 = _df['city'] == 'Москва', _df['city'] == 'Другое'
        tatle1, tatle2 = 'Moscow', 'Other'
    else:
        raise Exception('Wrong hist type: ' + hist_type)
    
    DATA1 = _df[condition1][col_name]
    DATA2 = _df[condition2][col_name]
    
    fig = plt.figure(figsize=(16, 6))
    ax1 = fig.add_subplot(121)
    st.probplot(DATA1, plot=ax1)
    ax1.set_title(tatle1)
    
    ax2 = fig.add_subplot(122)
    st.probplot(DATA2, plot=ax2)
    ax2.set_title(tatle2)
    plt.show()

# ========================================================================================================
# Выводит распределение переданных значений и теоретическое нормальное распределение.
# ========================================================================================================

def show_normal_distribution_over_hist(_df, hist_type, col_name, title):
    condition1, condition2 = None, None
    title_part = 'Distribution of the ' + title
    
    if hist_type == PLOT_TYPE_TARIFF:
        condition1, condition2 = _df['tariff'] == 'smart', _df['tariff'] == 'ultra'
        tatle1, tatle2 = title_part + ' (tariff Smart)', title_part + ' (tariff Ultra)'
    elif hist_type == PLOT_TYPE_LOCATION:
        condition1, condition2 = _df['city'] == 'Москва', _df['city'] == 'Другое'
        tatle1, tatle2 = title_part + ' (Moscow)', title_part + ' (Other)'
    else:
        raise Exception('Wrong hist type: ' + hist_type)
    
    DATA1 = _df[condition1][col_name]
    DATA2 = _df[condition2][col_name]
    
    
    mean, std = st.norm.fit(DATA1)
    x = np.linspace(DATA1.min(), DATA1.max(), len(DATA1))
    y = st.norm.pdf(x, mean, std)

    fig = plt.figure(figsize=(16, 6))
    ax1 = fig.add_subplot(121)
    DATA1.plot(kind='hist', ax=ax1, bins=30, alpha=0.4, ec='black', color='blue', density=True, title=tatle1)
    plt.plot(x,y, color='red')
    plt.legend(['Theoretical normal distribution', 'Real distribution'], prop={'size':12})
    vals = ax1.get_yticks()
    ax1.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
    
    mean, std = st.norm.fit(DATA2)
    x = np.linspace(DATA2.min(), DATA2.max(), len(DATA2))
    y = st.norm.pdf(x, mean, std)
    
    ax2 = fig.add_subplot(122)
    DATA2.plot(kind='hist', ax=ax2, bins=30, alpha=0.4, ec='black', color='blue', density=True, title=tatle2)
    plt.plot(x,y, color='red')
    plt.legend(['Theoretical normal distribution', 'Real distribution'], prop={'size':12})
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
    
    plt.show()