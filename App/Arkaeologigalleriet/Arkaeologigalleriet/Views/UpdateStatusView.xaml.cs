using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class UpdateStatusView : ContentPage
{
    private readonly UpdateStatusViewModel _vm;

    public UpdateStatusView(UpdateStatusViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
        _vm = vm;
    }

    protected override void OnNavigatedTo(NavigatedToEventArgs args)
    {
        base.OnNavigatedTo(args);
        _vm.GetArtefact();
    }
}