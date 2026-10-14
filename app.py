import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    from marimo import ui
    import io

    return io, mo, pd, px, ui


@app.cell
def _(mo):
    mo.md(f"""
    Upload a CSV file with the following fields names: Product_Id, Month, Unit_Sales, Product_Name
    """)
    return


@app.cell
def _(mo):
    # Create a file upload widget (supports up to 100MB)
    file_upload = mo.ui.file(filetypes=[".csv"], kind="area")
    file_upload
    return (file_upload,)


@app.cell
def _(file_upload, io, pd):
    if file_upload.contents():
        # Pass the byte data into pandas using io.BytesIO
        dataset = pd.read_csv(io.BytesIO(file_upload.contents()))
    else:
        "Please upload a CSV file above."
    return (dataset,)


@app.cell
def _(dataset):
    dataset
    return


@app.cell
def _(dataset, mo, ui):
    products = dataset['Product_Name'].unique()

    product_selector = ui.multiselect(
        products, label="Select products", value=["Berry Juice"]
    )

    mo.md(f"Choose a product: {product_selector}")

    product_selector
    return (product_selector,)


@app.cell
def _(mo, ui):
    chart_type = ui.dropdown(["Line", "Bar"], label="Chart Type", value="Line")

    mo.md(f"Choose a chart type: {chart_type}")

    chart_type
    return (chart_type,)


@app.cell
def _(chart_type, dataset, product_selector, px):
    # Filter data for selected products
    plot_data = dataset[dataset["Product_Name"].isin(product_selector.value)]

    # Create plot based on selection
    if chart_type.value == "Line":
        fig = px.line(
            plot_data,
            x="Month",
            y="Unit_Sales",
            color="Product_Name",
            title="Sales Trends",
        )
    else:
        fig = px.bar(
            plot_data,
            x="Month",
            y="Unit_Sales",
            color="Product_Name",
            title="Monthly Sales",
            barmode="group",
        )
    fig
    return


if __name__ == "__main__":
    app.run()
