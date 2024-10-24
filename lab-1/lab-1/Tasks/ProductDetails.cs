namespace lab_1.Tasks;

public class ProductDetails
{
    public string Name { set; get; }
    public string PriceCurrency { get; set; }
    public int PriceAmount { get; set; }
    public string ProductLink { get; set; }
    public Dictionary<string, string> ProductParameters { get; set; }

    public ProductDetails(string name, string priceCurrency, int priceAmount, string productLink,
        Dictionary<string, string> productParameters)
    {
        Name = name;
        PriceCurrency = priceCurrency;
        PriceAmount = priceAmount;
        ProductLink = productLink;
        ProductParameters = productParameters;
    }
    
    public void PrintDetails()
    {
        Console.WriteLine($"Product Name: {Name}");
        Console.WriteLine($"Price: {PriceAmount} {PriceCurrency}");
        Console.WriteLine($"Product Link: {ProductLink}");

        if (ProductParameters != null && ProductParameters.Count > 0)
        {
            Console.WriteLine("Product Parameters:");
            foreach (var param in ProductParameters)
            {
                Console.WriteLine($"{param.Key}: {param.Value}");
            }
        }
        else
        {
            Console.WriteLine("No parameters available.");
        }
    }
}