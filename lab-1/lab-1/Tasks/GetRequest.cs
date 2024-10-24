namespace lab_1.Tasks;
using System;
using System.Net.Http;
using System.Threading.Tasks;


public class GetRequest
{
    private readonly HttpClient _httpClient;

    public GetRequest()
    {
        _httpClient = new HttpClient();
    }

    public async Task<string> FetchSiteContent(string url)
    {
        try
        {
            HttpResponseMessage response = await _httpClient.GetAsync(url);

            if (response.IsSuccessStatusCode)
            {
                string htmlContent = await response.Content.ReadAsStringAsync();
                return htmlContent;
            }
            else
            {
                return $"Error: Unable to fetch the website. StatusCode: {response.StatusCode}";
            }
        }
        catch (Exception ex)
        {
            return $"Exception: {ex.Message}";
        }
    }

}