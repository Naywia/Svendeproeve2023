using Arkaeologigalleriet.Models;
using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class SearchView : ContentPage
{
    private readonly SearchViewModel _vm;

    public SearchView(SearchViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
        _vm = vm;
    }
    protected override void OnNavigatedTo(NavigatedToEventArgs args)
    {
        base.OnNavigatedTo(args);
        _vm.GetAllArtefacts();
    }
   
}