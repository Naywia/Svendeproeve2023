using Arkaeologigalleriet.ViewModels;
using Arkaeologigalleriet.Views;
using CommunityToolkit.Maui;
using Microsoft.Extensions.Logging;

namespace Arkaeologigalleriet;

public static class MauiProgram
{
	public static MauiApp CreateMauiApp()
	{
		var builder = MauiApp.CreateBuilder();
		builder
			.UseMauiApp<App>()            
            .UseMauiCommunityToolkit()
            .ConfigureFonts(fonts =>
			{
				fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
				fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
			});

		builder.Services.AddSingleton<MainPage>();
		builder.Services.AddSingleton<MainPageViewModel>();

        builder.Services.AddTransient<EmployeeView>();
        builder.Services.AddTransient<EmployeeViewModel>();

        builder.Services.AddTransient<SearchView>();
        builder.Services.AddTransient<SearchViewModel>();

        builder.Services.AddTransient<ScanQRView>();
        builder.Services.AddTransient<ScanQRViewModel>();

        builder.Services.AddTransient<ChangePasswordView>();
        builder.Services.AddTransient<ChangePasswordViewModel>();

        builder.Services.AddTransient<ArtifactInformationView>();
        builder.Services.AddTransient<ArtifactInformationViewModel>();

        builder.Services.AddTransient<UpdateStatusView>();
        builder.Services.AddTransient<UpdateStatusViewModel>();


#if DEBUG
        builder.Logging.AddDebug();
#endif

		return builder.Build();
	}
}
