import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { MapsPage } from './maps';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';


@NgModule({
  declarations: [
    MapsPage,
  ],
  exports: [
    MapsPage
  ],
  imports: [
    IonicPageModule.forChild(MapsPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class MapsPageModule {}
