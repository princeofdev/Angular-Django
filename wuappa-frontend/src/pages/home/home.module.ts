import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { HomePage } from './home';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';
@NgModule({
    declarations: [HomePage],
    exports: [HomePage],
    imports: [
        IonicPageModule.forChild(HomePage),
        TranslateModule,
        ComponentsModule
    ],
})
export class HomePageModule { }
