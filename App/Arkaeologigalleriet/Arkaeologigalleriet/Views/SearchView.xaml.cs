using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class SearchView : ContentPage
{
	public SearchView(SearchViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
		
		
	}
}