using Arkaeologigalleriet.Models;
using Arkaeologigalleriet.Services;
using Arkaeologigalleriet.Views;
using CommunityToolkit.Maui.Core.Extensions;
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
    public partial class UpdateStatusViewModel : BaseViewModel
    {

        ApiServices _apiServices;

        private int _newPlacmentId;

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

        private ObservableCollection<PlacementModel> _placements;

        public ObservableCollection<PlacementModel> Placements
        {
            get { return _placements; }
            set
            {
                _placements = value; 
                OnPropertyChanged(nameof(Placements));
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
                }
            }
        }

        private List<PlacementModel> _placementModels;

        public List<PlacementModel> PlacementModels
        {
            get { return _placementModels; }
            set 
            {
                _placementModels = value; 
                OnPropertyChanged(nameof(PlacementModels));
            }
        }


        private PlacementModel _selectedeplacement;

        public PlacementModel Selectedeplacement
        {
            get { return _selectedeplacement; }
            set 
            {
                _selectedeplacement = value; 
                OnPropertyChanged(nameof(Selectedeplacement));
            }
        }



        public UpdateStatusViewModel()
        {
            _apiServices = new();
            Placements = new ObservableCollection<PlacementModel>();
            LoadDataAsync();
        }

        private async Task LoadDataAsync()
        {
            await GetStorages();
        }

        public async Task GetStorages()
        {
            Storages = new ObservableCollection<StorageModel>();
            var getListFomrApi = await _apiServices.GetStorage();
            Storages = getListFomrApi.ToObservableCollection();
            PlacementModels = new List<PlacementModel>();
            PlacementModels = await _apiServices.GetPlacementModelsAsync();
            Placements = PlacementModels.ToObservableCollection();
        }

        public async void GetArtefact()
        {
            Artefacts = new ObservableCollection<Artefact>();
            List<Artefact> artefacts = await _apiServices.GetArtefactAsync(ArtifactID);
            Artefacts = artefacts.ToObservableCollection();
        }

        

        [RelayCommand]
        private void UpdatePlacements()
        {
            Placements = new ObservableCollection<PlacementModel>(_placementModels.Where(p => p.Storage == SelectedStorage.Name));
        }

        [RelayCommand]
        private void GetPlacementID()
        {
            _newPlacmentId = Selectedeplacement.ID;
        }

        [RelayCommand]
        private async void CancelUpdate()
        {
            await AppShell.Current.GoToAsync($"..");
        }

        [RelayCommand]
        private async void SaveNewPlacmentAsync()
        {
            if (await _apiServices.UpdatePlacmentOnArtefact(ArtifactID, _newPlacmentId))
            {
                await Application.Current.MainPage.DisplayAlert("Opdateret", "Placment er opdateret.", "Ok");
                await AppShell.Current.GoToAsync("..");
            }
            else
            {
                await Application.Current.MainPage.DisplayAlert("Fejl", "Der skete en fejl. Prøv igen", "Ok");
            }
        }

        
    }
}
