<<<<<<< HEAD
<<<<<<< HEAD
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import shap
from sklearn.ensemble import GradientBoostingClassifier
from streamlit_shap import st_shap

# Display Wal-Mart Labs logo.
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Walmart_Labs_logo.svg/1024px-Walmart_Labs_logo.svg.png" )

st.markdown("<h1 style='text-align: center; color: black;'>Online Electronics Purchasing Behavior</h1>", unsafe_allow_html=True)

# Import train dataset to DataFrame
train_df = pd.read_csv("/home/kingos82/Fourthbrain/MLE-11/assignments/week-06-supervised-ml/dat/train.csv.gz", compression="gzip")
test_df = pd.read_csv("/home/kingos82/Fourthbrain/MLE-11/assignments/week-06-supervised-ml/dat/test.csv.gz", compression="gzip")
model_results_df = pd.read_csv("/home/kingos82/Fourthbrain/MLE-11/assignments/week-06-supervised-ml/dat/model_results.csv")
X_test_reduced_df = pd.read_csv("/home/kingos82/Fourthbrain/MLE-11/assignments/week-06-supervised-ml/dat/X_test_reduced_df.csv")
X_test_reduced=X_test_reduced_df.to_numpy()
X_train_reduced_df = pd.read_csv("/home/kingos82/Fourthbrain/MLE-11/assignments/week-06-supervised-ml/dat/X_train_reduced_df.csv")
X_train_reduced=X_train_reduced_df.to_numpy()
y_train_df = pd.read_csv("/home/kingos82/Fourthbrain/MLE-11/assignments/week-06-supervised-ml/dat/y_train_df.csv")
y_train=y_train_df.to_numpy()
y_train=y_train[:,1]

# Drop uniformative columns
train_df.drop(columns=["year", "month", "Weekend"], inplace=True)


# Create sidebar for user selection
with st.sidebar:
    # Add FB logo
    st.image("https://user-images.githubusercontent.com/37101144/161836199-fdb0219d-0361-4988-bf26-48b0fad160a3.png" )    

    # Available models for selection
    models = ["Logistic Regression", "SVM", "Gradient Boosting Classifier"]

    # Add model select boxes
    model1_select = st.selectbox(
        "Choose Model 1:",
        ("Logistic Regression", "SVM", "Gradient Boosting Classifier")
    )
    
    # Remove selected model 1 from model list
    # App refreshes with every selection change.
    models.remove(model1_select)
    
    model2_select = st.selectbox(
        "Choose Model 2:",
        (models)
    )

# Create tabs for separation of tasks
tab1, tab2, tab3 = st.tabs(["???? Data", "???? Model Results", "???? Model Explainability"])

with tab1:    
    # Data Section Header
    st.header("Raw Data")

    # Display first 100 samples of the dateframe
    st.dataframe(train_df.head(100))

    st.header("Correlations")

    # Heatmap
    corr = train_df.corr()
    fig = px.imshow(corr)
    st.write(fig)

with tab2:    
    
    # Columns for side-by-side model comparison
    col1, col2 = st.columns(2)


    cols = ["tn", "fp", "fn", "tp"]

    model1_results = model_results_df[model_results_df["model"] == model1_select]
    cm1  = model1_results[cols].to_numpy()[0].reshape(2,2).tolist()

    x1 = ["0", "1"]
    y1 = ["1", "0"]
    z1 = cm1
    z_text1 = [[str(y) for y in x] for x in z1]


    # Build the confusion matrix for the first model.
    with col1:
        st.header(model1_select)

        fig1 = px.imshow(z1, text_auto=True)
        
        # add custom x-axis title
        fig1.add_annotation(dict(font=dict(color="black",size=14),
                                x=0.5,
                                y=-0.00005,
                                showarrow=False,
                                text="Predicted value",
                                xref="paper",
                                yref="paper"))

        # add custom y-axis title
        fig1.add_annotation(dict(font=dict(color="black",size=14),
                                x=-0.25,
                                y=0.5,
                                showarrow=False,
                                text="True value",
                                textangle=-90,
                                xref="paper",
                                yref="paper"))


        # Write plotly chart and fit to the container width.
        st.plotly_chart(fig1, use_container_width=True)

    # Build confusion matrix for second model
    with col2:
        model2_results = model_results_df[model_results_df["model"] == model2_select]
        cm2  = model2_results[cols].to_numpy()[0].reshape(2,2).tolist()

        x2 = ["0", "1"]
        y2 = ["1", "0"]
        z2 = cm2
        z_text2 = [[str(y) for y in x] for x in z2]

        st.header(model2_select)

        fig2 = px.imshow(z2, text_auto=True)
        
        # add custom x-axis title
        fig2.add_annotation(dict(font=dict(color="black",size=14),
                                x=0.5,
                                y=-0.00005,
                                showarrow=False,
                                text="Predicted value",
                                xref="paper",
                                yref="paper"))

        # add custom y-axis title
        fig2.add_annotation(dict(font=dict(color="black",size=14),
                                x=-0.25,
                                y=0.5,
                                showarrow=False,
                                text="True value",
                                textangle=-90,
                                xref="paper",
                                yref="paper"))



        
        # Write plotly chart and fit to the container width.
        st.plotly_chart(fig2, use_container_width=True)

with tab3: 
    # YOUR CODE GOES HERE!
        # Use tab2 as a guide!  
        # Use columns to separate visualizations for models
        # Include a plot for local and global explanability!
    col1, col2 = st.columns(2)
    with col1:

        np.random.seed(123)
        subset_size = 10000 #X_test_reduced.shape[0] # start with 100
        idx = np.random.randint(X_test_reduced.shape[0], size=subset_size)
        X_test_reduced_subset = X_test_reduced[idx, ]

        gbt_model = GradientBoostingClassifier() # YOUR CODE HERE
        gbt_model.fit(X_train_reduced, y_train)
        explainer = shap.Explainer(gbt_model)
        shap_values = explainer(X_test_reduced_subset)
        st.header(model1_select)
        st_shap(shap.plots.beeswarm(shap_values), height=300)
        
    
    with col2:
        subset_size = X_test_reduced.shape[0] # start with 100
        idx = np.random.randint(X_test_reduced.shape[0], size=subset_size)
        X_test_reduced_subset = X_test_reduced[idx, ]
        explainer = shap.Explainer(gbt_model)
        shap_values = explainer(X_test_reduced_subset)
        st.header(model2_select)
        fig22=shap.plots.beeswarm(shap_values)
        st.write(fig22)

    
=======
=======
>>>>>>> f887c00 (cleaning up local PR)
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
import streamlit.components.v1 as components

# Display Wal-Mart Labs logo.
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Walmart_Labs_logo.svg/1024px-Walmart_Labs_logo.svg.png" )

st.markdown("<h1 style='text-align: center; color: black;'>Online Electronics Purchasing Behavior</h1>", unsafe_allow_html=True)

# Import train dataset to DataFrame
train_df = pd.read_csv("../dat/train.csv.gz", compression="gzip")
model_results_df = pd.read_csv("../dat/model_results.csv")

# Drop uniformative columns
train_df.drop(columns=["year", "month", "Weekend"], inplace=True)


# Create sidebar for user selection
with st.sidebar:
    # Add FB logo
    st.image("https://user-images.githubusercontent.com/37101144/161836199-fdb0219d-0361-4988-bf26-48b0fad160a3.png" )    

    # Available models for selection
    models = ["Logistic Regression", "SVM", "Gradient Boosting Classifier"]

    # Add model select boxes
    model1_select = st.selectbox(
        "Choose Model 1:",
        ("Logistic Regression", "SVM", "Gradient Boosting Classifier")
    )
    
    # Remove selected model 1 from model list
    # App refreshes with every selection change.
    models.remove(model1_select)
    
    model2_select = st.selectbox(
        "Choose Model 2:",
        (models)
    )

# Create tabs for separation of tasks
tab1, tab2, tab3 = st.tabs(["???? Data", "???? Model Results", "???? Model Explainability"])

with tab1:    
    # Data Section Header
    st.header("Raw Data")

    # Display first 100 samples of the dateframe
    st.dataframe(train_df.head(100))

    st.header("Correlations")

    # Heatmap
    corr = train_df.corr()
    fig = px.imshow(corr)
    st.write(fig)

with tab2:    
    
    # Columns for side-by-side model comparison
    col1, col2 = st.columns(2)


    cols = ["tn", "fp", "fn", "tp"]

    model1_results = model_results_df[model_results_df["model"] == model1_select]
    cm1  = model1_results[cols].to_numpy()[0].reshape(2,2).tolist()

    x1 = ["0", "1"]
    y1 = ["1", "0"]
    z1 = cm1
    z_text1 = [[str(y) for y in x] for x in z1]


    # Build the confusion matrix for the first model.
    with col1:
        st.header(model1_select)

        fig1 = px.imshow(z1, text_auto=True)
        
        # add custom x-axis title
        fig1.add_annotation(dict(font=dict(color="black",size=14),
                                x=0.5,
                                y=-0.00005,
                                showarrow=False,
                                text="Predicted value",
                                xref="paper",
                                yref="paper"))

        # add custom y-axis title
        fig1.add_annotation(dict(font=dict(color="black",size=14),
                                x=-0.25,
                                y=0.5,
                                showarrow=False,
                                text="True value",
                                textangle=-90,
                                xref="paper",
                                yref="paper"))


        # Write plotly chart and fit to the container width.
        st.plotly_chart(fig1, use_container_width=True)

    # Build confusion matrix for second model
    with col2:
        model2_results = model_results_df[model_results_df["model"] == model2_select]
        cm2  = model2_results[cols].to_numpy()[0].reshape(2,2).tolist()

        x2 = ["0", "1"]
        y2 = ["1", "0"]
        z2 = cm2
        z_text2 = [[str(y) for y in x] for x in z2]

        st.header(model2_select)

        fig2 = px.imshow(z2, text_auto=True)
        
        # add custom x-axis title
        fig2.add_annotation(dict(font=dict(color="black",size=14),
                                x=0.5,
                                y=-0.00005,
                                showarrow=False,
                                text="Predicted value",
                                xref="paper",
                                yref="paper"))

        # add custom y-axis title
        fig2.add_annotation(dict(font=dict(color="black",size=14),
                                x=-0.25,
                                y=0.5,
                                showarrow=False,
                                text="True value",
                                textangle=-90,
                                xref="paper",
                                yref="paper"))



        
        # Write plotly chart and fit to the container width.
        st.plotly_chart(fig2, use_container_width=True)

with tab3: 
    # YOUR CODE GOES HERE!
        # Use tab2 as a guide!  
        # Use columns to separate visualizations for models
        # Include a plot for local and global explanability!
     
    st.header(model1_select)
    
    st.header(model2_select)

    
<<<<<<< HEAD
>>>>>>> f887c00 (cleaning up local PR)
=======
>>>>>>> f887c00 (cleaning up local PR)
