import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { LoginAccessPage } from './login-access';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    LoginAccessPage,
  ],
  imports: [
    IonicPageModule.forChild(LoginAccessPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class LoginAccessPageModule {}
