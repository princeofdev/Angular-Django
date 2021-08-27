import { Injectable } from '@angular/core';
import { APIService } from './api-service';


@Injectable()
export class CardsService extends APIService {

    public getCards() {
      return this.http.get(this.getApiUrl("cards"));
    }

    public saveCard(card) {
      return this.http.post(this.getApiUrl("cards"), card);
    }

    public deleteCard(card) {
      const url = this.getApiUrl("cards") + card.id + '/';
      return this.http.delete(url);
    }


}
