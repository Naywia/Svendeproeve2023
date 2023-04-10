using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class ArtifactInformationView : ContentPage
{
    private readonly ArtifactInformationViewModel _vm;

    public ArtifactInformationView(ArtifactInformationViewModel vm)
	{
		InitializeComponent();       
        LoadArtecaftInfo();
        _vm = vm;
        BindingContext = vm;        
    }

	async void LoadArtecaftInfo()
	{
        await _vm.GetArtifact();
    }
}