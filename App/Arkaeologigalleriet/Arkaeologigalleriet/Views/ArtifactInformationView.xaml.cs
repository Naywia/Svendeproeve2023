using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class ArtifactInformationView : ContentPage
{
    private readonly ArtifactInformationViewModel _vm;

    public ArtifactInformationView(ArtifactInformationViewModel vm)
	{
		InitializeComponent(); 
        BindingContext = vm;
        _vm = vm;
    }
    protected override void OnNavigatedTo(NavigatedToEventArgs args)
    {
        base.OnNavigatedTo(args);
        _vm.GetArtifact();
    }
}