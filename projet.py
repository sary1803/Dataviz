import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import altair as alt

# Decorator
def deco(function):
    def modified_function(df):
        timer= time.time()
        resultat = function(df)
        timer = time.time()-timer
        with open(f"{function.__name__}_exec_time.txt","w") as f:
            f.write(f"{timer}")
        return resultat
    return modified_function
def main():
    def get_dom(dt):
            return dt.day
    def get_month(dt):
            return dt.month
    def get_hours(dt):
            return dt.hour

    #load data
   
    @st.cache
    def load_csv():
        df=pd.read_csv('https://jtellier.fr/DataViz/full_2020.csv')
        return df

    #Dealing with null values 
    @deco
    @st.cache
    def null_value(df):
        m_surface=df["surface_reelle_bati"].mean()
        m_valeur=df["valeur_fonciere"].mean()
        m_piece=df["nombre_pieces_principales"].mean()
        df["surface_reelle_bati"]=df["surface_reelle_bati"].fillna(m_surface)
        df["valeur_fonciere"]=df["valeur_fonciere"].fillna( m_valeur)
        df["nombre_pieces_principales"]=df["nombre_pieces_principales"].fillna( m_piece)

        return df
    def culture_null(df):
        df3=df["nature_culture"]

        return df3.dropna()
    # transform data
    @deco
    @st.cache 
    def data_transform(df):
        df.adresse_code_voie=df.adresse_code_voie.astype(str)

        df.code_commune=df.code_commune.astype(str)

        df.code_departement=df.code_departement.astype(str)

        df.numero_volume=df.numero_volume.astype(str)

        df.lot1_numero=df.lot1_numero.astype(str)

        df.lot2_numero=df.lot2_numero.astype(str)

        df.lot3_numero=df.lot3_numero.astype(str)

        df.lot4_numero=df.lot4_numero.astype(str)

        df.lot5_numero=df.lot5_numero.astype(str)

        df.date_mutation=pd.to_datetime(df.date_mutation)
        df.latitude=df.latitude.astype('float64')
        df.longitude=df.longitude.astype('float64')
        df.index = df.date_mutation
        df["date_mutation"] = df["date_mutation"].map(pd.to_datetime)
        df["date_mutation"]=pd.to_datetime(df["date_mutation"])
        df["Day"]=df["date_mutation"].map(get_dom)
        df["month"]=df["date_mutation"].map(get_month)
        df["hour"]=df["date_mutation"].map(get_hours)
        return df

    def data_map(df):
        df5=df[["latitude","longitude"]]
        df5.columns=["lat","lon"]
        return df5
    def price_groupby(df):
        df1=df[["valeur_fonciere","code_departement"]]
        return df1.groupby("code_departement").mean()
    def surface_groupby(df):
        df1=df[["surface_reelle_bati","code_departement"]]
        return df1.groupby("code_departement").mean()

    def piece_groupby(df):
        df1=df[["nombre_pieces_principales","code_departement"]]
        return df1.groupby("code_departement").mean()
    def mutation_group_by(df):
        df1=df[["id_mutation","month","code_departement"]]
        return df1.groupby(["month","code_departement"]).count()
    
    st.title(' Data Visualization project')
    st.write('Cette application vous permettra de visualiser les tarnsations immobilières en France courant 2020')
    df1=load_csv()
    df2=data_transform(df1)
    df=null_value(df2)
    option=st.selectbox('Choose one visualisation',['Description des données','Visualisation détaillée'])
    if option=='Description des données':
        st.caption("Données de 2020")
        st.write(df.describe)


    elif option=='Visualisation détaillée':
        
        st.caption("Repartition des biens immobilier sur le territoire français")
  
        st.map(data_map(df))
        st.caption("Prix moyen du metre carré en fonction du département")
    
        st.bar_chart(price_groupby(df))
        st.caption("surface reelle bati en fonction du département")
        
        st.bar_chart(surface_groupby(df))
        st.caption("nature des cultures")
        
        data=culture_null(df)
        data=data.value_counts()
        fig=sns.heatmap(data)
        st.pyplot(fig)
        st.caption("nombre moyen de chambre par département")
        
        st.bar_chart(piece_groupby(df))
        st.caption("Mutation par mois en fonction du departement")
    
        departement=df['code_departement'].unique().tolist()
        dep=st.selectbox('Sélectionner un département', departement, 0)
        donnee=mutation_group_by(df)
        labels=donnee["month"].unique().tolist()
        ex1=(0,0.1)

        fig1, ax1=plt.subplots()
        ax1.pie(donnee['count'], explode=ex1, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)

        ax1.axis('equal') 
if __name__=="__main__":
    main()
