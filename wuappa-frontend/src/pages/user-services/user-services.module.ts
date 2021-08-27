import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { UserServicesPage } from './user-services';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    UserServicesPage,
  ],
  exports: [
    UserServicesPage
  ],
  imports: [
    IonicPageModule.forChild(UserServicesPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class UserServicesPageModule {}
