def filter_dataframe(df, date_slider):

    dff = df.loc[
       (df.index >= df.index[int(date_slider[0])])
        & (df.index <= df.index[int(date_slider[1])]),:
    ].copy()
    
    return dff