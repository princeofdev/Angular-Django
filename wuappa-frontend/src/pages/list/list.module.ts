import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ListPage } from './list';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';
@NgModule({
    declarations: [ListPage],
    exports: [ListPage],
    imports: [
        IonicPageModule.forChild(ListPage),
        TranslateModule,
        ComponentsModule
    ],
})
export class ListPageModule { }
