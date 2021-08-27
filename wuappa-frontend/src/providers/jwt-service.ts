import { Injectable } from '@angular/core';
import { TokenService } from './token-service';


const REFRESH_TOKEN_TIME = 600000;    
@Injectable()

export class JWTService {

    constructor(private tokenService: TokenService) { }

    public checkToken() {
        setInterval(() => this.tokenService.refresh(), REFRESH_TOKEN_TIME);
    }

}
