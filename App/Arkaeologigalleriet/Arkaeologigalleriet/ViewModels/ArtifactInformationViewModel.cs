using Arkaeologigalleriet.Models;
using CommunityToolkit.Mvvm.ComponentModel;
using Newtonsoft.Json;
using System.Net.Http.Headers;

namespace Arkaeologigalleriet.ViewModels
{
    [QueryProperty(nameof(ArtifactID), nameof(ArtifactID))]
    public partial class ArtifactInformationViewModel : ObservableObject
    {
        HttpClient _client;
        string _url = "http://192.168.1.100:8000/";

        [ObservableProperty]
        Artefact _artifactModel;

        [ObservableProperty]
        int _artifactID;

        [ObservableProperty]
        string _name;

        [ObservableProperty]
        string _dec;

        public ArtifactInformationViewModel()
        {
        }

        

        public async Task<Artefact> GetArtifact()
        {
            ArtifactModel = new Artefact();
            _client = new HttpClient();

            try
            {
                using HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, _url + "artefact?artefactID=" + ArtifactID);
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await SecureStorage.Default.GetAsync("JWT"));
                HttpResponseMessage response = await _client.SendAsync(request);
                if (response.IsSuccessStatusCode)
                {                    
                    string payload = await response.Content.ReadAsStringAsync();
                    try
                    {
                        
                        var jsonModel = JsonConvert.DeserializeObject<ArtifactInformationModel>(payload);
                        foreach (var item in jsonModel.Artefact)
                        {
                            Name = item.Name;
                            Dec = item.Description;
                        }
                        
                    }
                    catch (Exception ex)
                    {
                        Console.Out.WriteLine(ex.Message);
                        throw;
                    }
                    return ArtifactModel;
                }
            }
            catch (Exception ex)
            {
                Console.Out.WriteLine(ex.Message);
                throw;
            }

            return null;
            
        }

        
    }
}
