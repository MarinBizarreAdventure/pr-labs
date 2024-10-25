namespace lab_1.Tasks;
using System.Text;
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
    
    public string SerializeToJson()
    {
        var jsonBuilder = new StringBuilder();
        jsonBuilder.Append("{");
        jsonBuilder.AppendFormat("\"Name\": \"{0}\",", Name);
        jsonBuilder.AppendFormat("\"PriceCurrency\": \"{0}\",", PriceCurrency);
        jsonBuilder.AppendFormat("\"PriceAmount\": {0},", PriceAmount);
        jsonBuilder.AppendFormat("\"Link\": \"{0}\",", ProductLink);

        jsonBuilder.Append("\"Parameters\": {");
        foreach (var param in ProductParameters)
        {
            jsonBuilder.AppendFormat("\"{0}\": \"{1}\",", param.Key, param.Value);
        }
        if (ProductParameters.Count > 0)
        {
            jsonBuilder.Length--; 
        }
        jsonBuilder.Append("}");

        jsonBuilder.Append("}");

        return jsonBuilder.ToString();
    }
    
    public string SerializeToXml()
    {
        var xmlBuilder = new StringBuilder();
        xmlBuilder.Append("<ProductDetails>");
        xmlBuilder.AppendFormat("<Name>{0}</Name>", Name);
        xmlBuilder.AppendFormat("<PriceCurrency>{0}</PriceCurrency>", PriceCurrency);
        xmlBuilder.AppendFormat("<PriceAmount>{0}</PriceAmount>", PriceAmount);
        xmlBuilder.AppendFormat("<Link>{0}</Link>", ProductLink);

        xmlBuilder.Append("<Parameters>");
        foreach (var param in ProductParameters)
        {
            xmlBuilder.AppendFormat("<{0}>{1}</{0}>", param.Key, param.Value);
        }
        xmlBuilder.Append("</Parameters>");

        xmlBuilder.Append("</ProductDetails>");

        return xmlBuilder.ToString();
    }
    
    
    public static ProductDetails CustomDeserialize(string serializedData)
    {
        var parts = serializedData.Split('|');

        if (parts.Length != 5)
        {
            throw new FormatException("Invalid serialized data format");
        }

        var name = parts[0];
        var priceCurrency = parts[1];
        var priceAmount = int.Parse(parts[2]);
        var link = parts[3];

        var parameters = new Dictionary<string, string>();
        var paramString = parts[4].Trim('{', '}');
        var paramPairs = paramString.Split(',');

        foreach (var pair in paramPairs)
        {
            var keyValue = pair.Split('=');
            if (keyValue.Length == 2)
            {
                parameters[keyValue[0]] = keyValue[1];
            }
        }

        return new ProductDetails(name, priceCurrency, priceAmount, link, parameters);
    }
    
    public string CustomSerialize()
    {
        var serializedString = new StringBuilder();

        serializedString.Append(Name).Append("|");
        serializedString.Append(PriceCurrency).Append("|");
        serializedString.Append(PriceAmount).Append("|");
        serializedString.Append(ProductLink).Append("|");

        serializedString.Append("{");
        foreach (var param in ProductParameters)
        {
            serializedString.AppendFormat("{0}={1},", param.Key, param.Value);
        }
        if (ProductParameters.Count > 0)
        {
            serializedString.Length--; 
        }
        serializedString.Append("}");

        return serializedString.ToString();
    }

}