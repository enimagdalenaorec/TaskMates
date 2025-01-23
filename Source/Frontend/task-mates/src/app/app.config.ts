import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideClientHydration } from '@angular/platform-browser';
import { BrowserAnimationsModule, provideAnimations } from '@angular/platform-browser/animations';
import { HTTP_INTERCEPTORS, HttpClientModule, HttpClient } from '@angular/common/http';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { importProvidersFrom } from '@angular/core';
import { routes } from './app.routes'; // Ensure you have the correct path to your routes
import { MyHttpInterceptor } from './Services/Interceptor/http-interceptor.interceptor'; // Ensure you have the correct path to your interceptor
import { InjectionToken } from '@angular/core';
import { TextFieldModule } from '@angular/cdk/text-field';
import { MatInputModule } from '@angular/material/input';
import { CustomMessageInputComponent } from './custom-message-input/custom-message-input.component';


export function httpLoaderFactory(http: HttpClient): TranslateHttpLoader {
  return new TranslateHttpLoader(http);
}

export const textareaInjectionToken = new InjectionToken<string>('textareaInjectionToken');

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideClientHydration(),
    provideAnimations(),
    {
      provide: HTTP_INTERCEPTORS,
      useClass: MyHttpInterceptor,
      multi: true,
    },
    importProvidersFrom(BrowserAnimationsModule,MatInputModule),

    importProvidersFrom(
      HttpClientModule,
      BrowserAnimationsModule,
      TextFieldModule,
      TranslateModule.forRoot({
        loader: {
          provide: TranslateLoader,
          useFactory: httpLoaderFactory,
          deps: [HttpClient],
        },
      }),
    ),
    { provide: textareaInjectionToken, useValue: CustomMessageInputComponent },
  ],
};
