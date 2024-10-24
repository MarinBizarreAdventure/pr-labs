namespace lab_1.Tasks;

public class FilteredProductDetails
{
    public List<ProductDetails> FilteredProducts { get; set; }
    public int TotalSum { get; set; }
    public DateTime TimeStamp { get; set; }
    
    public FilteredProductDetails(List<ProductDetails> filteredProducts, int totalSum)
    {
        FilteredProducts = filteredProducts;
        TotalSum = totalSum;
        TimeStamp = DateTime.UtcNow;
    }
    
    public void PrintResults()
    {
        Console.WriteLine($"Total Sum: {TotalSum}");
        Console.WriteLine($"Timestamp: {TimeStamp}");

        foreach (var product in FilteredProducts)
        {
            Console.WriteLine($"Product: {product.Name}, Price: {product.PriceAmount} {product.PriceCurrency}, Link: {product.ProductLink}");
        }
    }
}