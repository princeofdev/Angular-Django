import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule, CUSTOM_ELEMENTS_SCHEMA, Injector } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';

import { DatePipe } from '@angular/common';
import { HttpClientModule, HttpClient, HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';

import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { Camera } from '@ionic-native/camera';
import { IonicStorageModule } from '@ionic/storage';
import { Facebook } from '@ionic-native/facebook';
import { AgmCoreModule } from '@agm/core';
import { Geolocation } from '@ionic-native/geolocation';
import { NativeGeocoder } from '@ionic-native/native-geocoder';
import { Push } from '@ionic-native/push';
import { Keyboard } from '@ionic-native/keyboard';
import { MyApp } from './app.component';
import { UserService } from '../providers/user-service';
import { SessionService } from '../providers/session-service';
import {APIService} from '../providers/api-service';
import { SignupService } from '../providers/signup-service';
import { JWTService } from '../providers/jwt-service';
import { RequestsInterceptor } from '../providers/interceptor';
import { TokenService } from '../providers/token-service';
import { LocationService } from '../providers/location-service';
import { UploadService } from '../providers/upload-service';
import { ServicesService } from '../providers/services-service';
import { HireService } from '../providers/hire-service';
import { ValidateService } from '../providers/validate-service';
import { AppointmentService } from '../providers/appointment-service';
import { CardsService } from '../providers/cards-service';
import { CalendarService } from '../providers/calendar-service';
import { CalendarModule } from "ion2-calendar";
import { MAPS_API_KEY } from './constants';
import { ComponentsModule } from '../components/components.module';
//PAGE MODULES
import { AccountPageModule } from '../pages/account-page/account-page.module';
import { AddCardPageModule } from '../pages/add-card/add-card.module';
import { AppointmentDetailPageModule } from '../pages/appointment-detail/appointment-detail.module';
import { AppointmentsPageModule } from '../pages/appointments/appointments.module';
import { ChangePasswordPageModule } from '../pages/change-password/change-password.module';
import { CompleteRecoverPasswordPageModule } from '../pages/complete-recover-password/complete-recover-password.module';
import { ConfirmAddressPageModule } from '../pages/confirm-address/confirm-address.module';
import { DocumentationPageModule } from '../pages/documentation-page/documentation-page.module';
import { FinishOrderPageModule } from '../pages/finish-order/finish-order.module';
import { HomePageModule } from '../pages/home/home.module';
import { LoginPageModule } from '../pages/login/login.module';
import { MapsPageModule } from '../pages/maps/maps.module';
import { MenuPageModule } from '../pages/menu/menu.module';
import { MobileConfirmationPageModule } from '../pages/mobile-confirmation/mobile.confirmation.module';
import { PaymentMethodPageModule } from '../pages/payment-method/payment-method.module';
import { ResumePageModule } from '../pages/resume-page/resume-page.module';
import { ServiceBasketPageModule } from '../pages/service-basket/service-basket.module';
import { ServicesPageModule } from '../pages/services-page/services-page.module';
import { SettingsPageModule } from '../pages/settings/settings.module';
import { SignupPageModule } from '../pages/signup/signup.module';
import { SignupAddPicturePageModule } from '../pages/signup-add-picture/signup-add-picture.module';
import { SignupConfirmationPageModule } from '../pages/signup-confirmation/signup-confirmation.module';
import { TermsConditionsPageModule } from '../pages/terms-conditions/terms-conditions.module';
import { UserCalendarPageModule } from '../pages/user-calendar/user-calendar.module';
import { UserServicesPageModule } from '../pages/user-services/user-services.module';
import { WorkCalendarPageModule } from '../pages/work-calendar/work-calendar.module';
import { WorkDaysPageModule } from '../pages/work-days/work-days.module';
import { WorkZonePageModule } from '../pages/work-zone/work-zone.module';
import { RecoverPasswordPageModule } from '../pages/recover-password/recover-password.module';
import { WorkZoneDistrictPageModule } from '../pages/work-zone-district/work-zone-district.module';
import { ListPageModule } from '../pages/list/list.module';
import { TermsConditionsMenuPageModule } from '../pages/terms-conditions-menu/terms-conditions-menu.module';
import { ServiceDetailPageModule } from '../pages/service-detail/service-detail.module';
import { HelpPageModule } from '../pages/help/help.module';
import { LoginAccessPageModule } from '../pages/login-access/login-access.module'
import { PipesModule } from '../pipes/pipes.module';
import { Globalization } from '@ionic-native/globalization';
import { SocialSharing } from '@ionic-native/social-sharing';


// AoT requires an exported function for factories
export function HttpLoaderFactory(http: HttpClient) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}

@NgModule({
  declarations: [
    MyApp
    ],
  schemas: [ CUSTOM_ELEMENTS_SCHEMA ],
  imports: [
    BrowserModule,
    CalendarModule,
    IonicModule.forRoot(MyApp, {
      backButtonText: '',
    },  {
      links: []
    }),
    AgmCoreModule.forRoot({
      apiKey: MAPS_API_KEY,
      libraries: ["places"]
    }),
    IonicStorageModule.forRoot(),
    HttpClientModule,
    HttpModule,
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: (HttpLoaderFactory),
        deps: [HttpClient]
      }
    }),
    FormsModule,
    AccountPageModule,
    AddCardPageModule,
    AppointmentDetailPageModule,
    AppointmentsPageModule,
    ChangePasswordPageModule,
    CompleteRecoverPasswordPageModule,
    ConfirmAddressPageModule,
    DocumentationPageModule,
    FinishOrderPageModule,
    HomePageModule,
    LoginPageModule,
    MapsPageModule,
    MenuPageModule,
    MobileConfirmationPageModule,
    PaymentMethodPageModule,
    RecoverPasswordPageModule,
    ResumePageModule,
    ServiceBasketPageModule,
    ServicesPageModule,
    SettingsPageModule,
    SignupPageModule,
    SignupAddPicturePageModule,
    SignupConfirmationPageModule,
    TermsConditionsPageModule,
    UserCalendarPageModule,
    UserServicesPageModule,
    WorkCalendarPageModule,
    WorkDaysPageModule,
    WorkZonePageModule,
    WorkZoneDistrictPageModule,
    ListPageModule,
    ComponentsModule,
    TermsConditionsMenuPageModule,
    ServiceDetailPageModule,
    HelpPageModule,
    LoginAccessPageModule,
    PipesModule
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp
  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    Camera,
    SessionService,
    UserService,
    APIService,
    TokenService,
    SignupService,
    LocationService,
    Facebook,
    IonicStorageModule,
    UploadService,
    JWTService,
    ServicesService,
    HireService,
    DatePipe,
    ValidateService,
    Geolocation,
    NativeGeocoder,
    AppointmentService,
    {provide: HTTP_INTERCEPTORS, useClass: RequestsInterceptor, multi: true, deps: [Injector] },
    CardsService,
    CalendarService,
    Push,
    Keyboard,
    Globalization,
    SocialSharing
  ]
})
export class AppModule {}
