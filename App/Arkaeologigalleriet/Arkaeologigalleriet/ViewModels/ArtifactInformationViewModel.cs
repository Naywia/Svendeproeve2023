using Arkaeologigalleriet.Models;
using Arkaeologigalleriet.Services;
using Arkaeologigalleriet.Views;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Media;
using Newtonsoft.Json;
using System.Diagnostics;
using System.Net.Http.Headers;

namespace Arkaeologigalleriet.ViewModels
{
    [QueryProperty(nameof(ArtifactID), nameof(ArtifactID))]
    public partial class ArtifactInformationViewModel : ObservableObject
    {
        #region Propyties

        ApiServices _apiServices;

        HttpClient _client;
        //string _url = "http://192.168.1.100:8000/";
        string _url = "http://164.68.113.72:8000/";

        [ObservableProperty]
        Artefact _artifactModel;

        [ObservableProperty]
        int _artifactID;

        [ObservableProperty]
        ImageSource _imageSource;

        [ObservableProperty]
        string _placmentString;

        [ObservableProperty]
        bool _TTSknapText = true;
        [ObservableProperty]
        bool _TTSStop = false;

        CancellationTokenSource _cts;

    

        #endregion

        public ArtifactInformationViewModel()
        {
            _apiServices = new();
        }


        #region ApiCall

        
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
                        ArtifactModel = jsonModel.Artefact.FirstOrDefault();
                        var placment = await _apiServices.GetSingelPlacementModelsAsync(ArtifactModel.PlacementID);
                        PlacmentString = placment.FirstOrDefault().DisplayText;
                        
                        if (!string.IsNullOrEmpty(ArtifactModel.ArtefactImage))
                        {
                            MemoryStream stream = new(Convert.FromBase64String(ArtifactModel.ArtefactImage));
                            ImageSource = ImageSource.FromStream(() => stream);
                        }
                        else
                        {

                            ImageSource = ImageSource.FromFile("snart.png");
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
        #endregion

        [RelayCommand]
        public async Task SpeakNowAsync()
        {
            _cts = new CancellationTokenSource();

            TTSknapText = false;
            TTSStop = true;
            IEnumerable<Locale> locales = await TextToSpeech.GetLocalesAsync();

            foreach (Locale locale in locales)
            {
                await Console.Out.WriteLineAsync(locale.Language);
            }


            SpeechOptions options = new SpeechOptions()
            {
                Pitch = 1.0f,   // 0.0 - 2.0
                Volume = 0.75f, // 0.0 - 1.0
            };

            await TextToSpeech.Default.SpeakAsync(ArtifactModel.Description, options, cancelToken: _cts.Token);

            TTSknapText = true;
            TTSStop = false;
        }

        [RelayCommand]
        public void CancelSpeech()
        {
            if (_cts?.IsCancellationRequested ?? true)
                return;

            _cts.Cancel();
            TTSknapText = true;
            TTSStop = false;
        }

        [RelayCommand]
        public async void NavigateToUpdate()
        {
            await Shell.Current.GoToAsync($"{nameof(UpdateStatusView)}?ArtifactID={ArtifactID}");
        }
    }
}
