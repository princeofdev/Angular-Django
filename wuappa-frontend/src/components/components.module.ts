import { NgModule, LOCALE_ID } from '@angular/core';
import { ImageUploaderComponent } from './image-uploader/image-uploader';
import { StaticMapsComponent } from './static-maps/static-maps';
import { MapSearchbarComponent } from './map-searchbar/map-searchbar';
import { ServiceCardComponent } from './service-card/service-card';
import { BasketItemComponent } from './basket-item/basket-item';
import { CalendarComponent } from './calendar/calendar';
import { AppointmentItemComponent } from './appointment-item/appointment-item';
import { PunctuationStarsComponent }  from './punctuation-stars/punctuation-stars';
import { NavbarComponent } from './navbar/navbar';
import { IonicPageModule } from 'ionic-angular/module';
import { TranslateModule } from '@ngx-translate/core';
import { CalendarModule } from 'ion2-calendar';
import { TermsComponent } from './terms/terms';
import { ProfileComponent } from './profile/profile';
import { CommonModule } from '@angular/common';
import { AppointmentServicesComponent } from './appointment-services/appointment-services';
import { PipesModule } from '../pipes/pipes.module';
import { CitiesCollapsableComponent } from './cities-collapsable/cities-collapsable';


@NgModule({
	declarations: [
        ImageUploaderComponent,
        StaticMapsComponent,
        MapSearchbarComponent,
        ServiceCardComponent,
        BasketItemComponent,
        CalendarComponent,
        PunctuationStarsComponent,
        NavbarComponent,
        AppointmentItemComponent,
        TermsComponent,
        ProfileComponent,
        AppointmentServicesComponent,
    CitiesCollapsableComponent
    ],
	imports: [
        CommonModule,
        IonicPageModule.forChild(NavbarComponent),
        IonicPageModule.forChild(ImageUploaderComponent),
        IonicPageModule.forChild(StaticMapsComponent),
        IonicPageModule.forChild(MapSearchbarComponent),
        IonicPageModule.forChild(ServiceCardComponent),
        IonicPageModule.forChild(BasketItemComponent),
        IonicPageModule.forChild(CalendarComponent),
        IonicPageModule.forChild(AppointmentItemComponent),
        IonicPageModule.forChild(PunctuationStarsComponent),
        TranslateModule,
        CalendarModule,
        IonicPageModule.forChild(CalendarModule),
        PipesModule
    ],
	exports: [
        ImageUploaderComponent,
        StaticMapsComponent,
        MapSearchbarComponent,
        ServiceCardComponent,
        BasketItemComponent,
        CalendarComponent,
        PunctuationStarsComponent,
        NavbarComponent,
        AppointmentItemComponent,
        TermsComponent,
        ProfileComponent,
        AppointmentServicesComponent,
    CitiesCollapsableComponent
    ],
    providers: [
        { provide: LOCALE_ID, useValue: "es" },
    ]
})
export class ComponentsModule {}
