import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AccountPage } from './account-page';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [AccountPage],
  exports: [AccountPage],
  imports: [
    IonicPageModule.forChild(AccountPage),
    TranslateModule,
    ComponentsModule,

  ],
})
export class AccountPageModule {}
