using Arkaeologigalleriet.Models;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Net.Http.Headers;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.ViewModels
{
    [QueryProperty(nameof(ArtifactID), nameof(ArtifactID))]
    public class UpdateStatusViewModel : INotifyPropertyChanged
    {

        HttpClient _client;
        //string _url = "http://192.168.1.100:8000/";
        string _url = "http://164.68.113.72:8000/";

        private int _artifactID;

        public int ArtifactID
        {
            get { return _artifactID; }
            set
            {
                _artifactID = value;
                OnPropertyChanged(nameof(ArtifactID));
            }
        }

        private ObservableCollection<StorageModel> _storages;

        public ObservableCollection<StorageModel> Storages
        {
            get { return _storages; }
            set
            {
                _storages = value;
                OnPropertyChanged(nameof(Storages));
            }
        }

        private ObservableCollection<Artefact> _artefacts;

        

        public ObservableCollection<Artefact> Artefacts
        {
            get { return _artefacts; }
            set 
            { 
                _artefacts = value; 
                OnPropertyChanged(nameof(Artefacts));
            }
        }

        private StorageModel _selectedStorage;

        public StorageModel SelectedStorage
        {
            get { return _selectedStorage; }
            set 
            { 
                
                if (_selectedStorage != value)
                {
                    _selectedStorage = value;
                    OnPropertyChanged(nameof(SelectedStorage));
                    UpdateArtefact();
                }
            }
        }




        public UpdateStatusViewModel()
        {
            GetStorages();
        }

        public async void GetStorages()
        {
            Storages = new ObservableCollection<StorageModel>();
            _client = new HttpClient();

            try
            {
                using HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, _url + "storage");
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await SecureStorage.Default.GetAsync("JWT"));
                HttpResponseMessage response = await _client.SendAsync(request);
                if (response.IsSuccessStatusCode)
                {
                    string payload = await response.Content.ReadAsStringAsync();
                    try
                    {
                        var jsonmodel = JsonConvert.DeserializeObject<StoragesListModel>(payload);
                        foreach (var item in jsonmodel.Storages)
                        {
                            Storages.Add(item);
                        }


                    }
                    catch (Exception ex)
                    {
                        await Console.Out.WriteLineAsync(ex.Message);
                        throw;
                    }
                }

            }
            catch (Exception ex)
            {
                await Console.Out.WriteLineAsync(ex.Message);
                throw;
            }            
            
        }

        public async void GetArtefact()
        {
            Artefacts = new ObservableCollection<Artefact>();
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
                        var jsonmodel = JsonConvert.DeserializeObject<ArtifactInformationModel>(payload);
                        foreach (var item in jsonmodel.Artefact)
                        {
                            Artefacts.Add(item);
                        }

                    }
                    catch (Exception ex)
                    {
                        await Console.Out.WriteLineAsync(ex.Message);
                        
                    }
                }
            }
            catch (Exception ex)
            {
                await Console.Out.WriteLineAsync(ex.Message);
                
            }
        }

        
        private void UpdateArtefact()
        {
            var testy = SelectedStorage;
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
