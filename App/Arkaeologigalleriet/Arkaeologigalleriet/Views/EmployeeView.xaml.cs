using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class EmployeeView : ContentPage
{

    public EmployeeView(EmployeeViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
    }

    protected override void OnNavigatedTo(NavigatedToEventArgs args)
    {
        base.OnNavigatedTo(args);
        
    }
}