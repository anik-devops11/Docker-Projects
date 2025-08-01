document.addEventListener('DOMContentLoaded', () => {
    const sendOtpForm = document.getElementById('send-otp-form');
    const verifyOtpForm = document.getElementById('verify-otp-form');
    const sendStatus = document.getElementById('send-status');
    const verifyStatus = document.getElementById('verify-status');


    sendOtpForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const phoneNumber = document.getElementById('phone-number').value;

        try {
        
            const response = await fetch('/generate-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ phone_number: phoneNumber })
            });

            const result = await response.json();
            
            if (response.ok) {
                sendStatus.textContent = `${result.message} - OTP: ${result.otp}`;
                sendStatus.style.color = 'green';
            } else {
                sendStatus.textContent = result.error;
                sendStatus.style.color = 'red';
            }
        } catch (error) {
            sendStatus.textContent = 'Something went wrong. Please try again.';
            sendStatus.style.color = 'red';
        }
    });

    
    verifyOtpForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const phoneNumber = document.getElementById('phone-number-verify').value;
        const otpCode = document.getElementById('otp-code').value;

        try {
          
            const response = await fetch('/verify-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ phone_number: phoneNumber, otp: otpCode })
            });

            const result = await response.json();
            
            if (response.ok) {
                verifyStatus.textContent = result.message;
                verifyStatus.style.color = 'green';
            } else {
                verifyStatus.textContent = result.error;
                verifyStatus.style.color = 'red';
            }
        } catch (error) {
            verifyStatus.textContent = 'Something went wrong. Please try again.';
            verifyStatus.style.color = 'red';
        }
    });
});