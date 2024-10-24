namespace lab_1.Tasks;

public class ProductFilterFactory
{
    private const double EURToMDL = 19.4368;
    private const double MDLToEUR = 0.0860;

    private List<ProductDetails> productDetailsList;

    public ProductFilterFactory(List<ProductDetails> productDetailsList)
    {
        this.productDetailsList = productDetailsList;
    }

    public FilteredProductDetails ProcessProducts(int minPrice, int maxPrice)
    {
        var convertedProducts = productDetailsList.Select(p =>
        {
            if (p.PriceCurrency == "EUR")
            {
                p.PriceAmount = (int)(p.PriceAmount * EURToMDL);
                p.PriceCurrency = "MDL";
            }
            else if (p.PriceCurrency == "MDL")
            {
                p.PriceAmount = (int)(p.PriceAmount * MDLToEUR);
                p.PriceCurrency = "EUR";
            }
            return p;
        }).ToList();

        var filteredProducts = convertedProducts.Where(p => p.PriceAmount >= minPrice && p.PriceAmount <= maxPrice).ToList();

        int totalSum = filteredProducts.Aggregate(0, (sum, product) => sum + product.PriceAmount);

        return new FilteredProductDetails(filteredProducts, totalSum);
    }
}
