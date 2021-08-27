import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { LoginPage } from './login';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [LoginPage],
  exports: [LoginPage],
  imports: [
    IonicPageModule.forChild(LoginPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class LoginPageModule {}
