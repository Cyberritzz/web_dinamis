    function processForm() {
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;

        if (username === '123' && password === '123') {
            Swal.fire({
                icon: 'success',
                title: 'Login Sukses!',
                text: 'Anda berhasil login.',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = 'http://localhost:8080/home';
                }
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Login Gagal!',
                text: 'Username atau password salah.',
                confirmButtonText: 'OK'
            });
        }
    }
