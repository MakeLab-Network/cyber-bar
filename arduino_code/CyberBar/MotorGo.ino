void motorGo(uint8_t motor, int pwm)         //Function that controls the variables: motor(0 or 1), direction (cw or ccw)  pwm (entra 0 e 255);
{

  // ------------------- Normalize pwm and direction ------------------------

  if (debugLevel >= 5) {
    //    if (motor == LEFT_MOTOR) debug(5, "powerLeft:", pwm); else debug(5, "powerRight:", pwm);
  }

  if (pwm > maxMotorPwm[motor]) pwm = maxMotorPwm[motor];                  // Bigger than max ? make it max
  else if (pwm < -maxMotorPwm[motor]) pwm = -maxMotorPwm[motor];           // Less than min, make it min

  // ------------- At this point pwm is in the range of -MAXPWM to MAXPWM and implies for the direction as well ------------------

  if (motor < NUM_OF_MOTORS) // check for valid motor
  {
    //      if (debugLevel>=5){debug(5, "motor ", motor);}

    // ############################################################################################
    // ---- Trying to make a smooth acceleration or de-acceleration.... hard coded for now for testing... formalize if it realy works... Avi -----
    // ---- The idea... if the gap from old PWN to new PWM is more than X (20) - get closer to it by taking old PWM and add "something" from that gap (for now.. 5%) -----------
    // ---- So.. if its 5% from the gap... by 20 itearation it will clear all gap (but even before... the gap will be less than X (20) and it will "jump" to the target PWM
    
/* // ---- No Acceleartion controlfor this application #################
    unsigned long timePassedFromLastMotorUpdate = millis() - lastMotorUpdateTime[motor];  // ###GUY - but what if long time since last update ? need ALSO max step anyway
    int maximumStepAllowed = int((maxAllowedPowerChangePerSecond[motor] * timePassedFromLastMotorUpdate) / 1000);
    maximumStepAllowed = min(maximumStepAllowed, maxMotorChangeAllowedWithBigStep[motor]); // if the step is too big we want to cap the power change anyway.

    if (pwm > oldPower[motor] + maximumStepAllowed) pwm = oldPower[motor] + maximumStepAllowed;        // accelerate/deaccelerate control
    else if ((pwm + maximumStepAllowed) < oldPower[motor]) pwm = oldPower[motor] - maximumStepAllowed; // deaccelerate/deaccelerate control

    oldPower[motor] = pwm;
*///  ###################
 
    //      oldDirection[motor] = direct; // this is only for slow breaking use (used by stopMotors). Note that this is the "normalized" direction - after the pwm normalized to be positive

    // ############################################################################################

    // ------------------ Actual update of motors here ####GUY - Should update for PCA ---------------------------
    if (motor == CONVEYOR_RIGHT_MOTOR) {
      rightMotor(pwm);
    }
    else if (motor == CONVEYOR_LEFT_MOTOR) {
      leftMotor(pwm);
    }
    // ----------------------------------------------------------------------------

    lastMotorUpdateTime[motor] = millis(); // remember the time we update the motors
  }                                        // If valid motors
}                       // End of motorGo function
