// a program that determines if
// a number n is prime
int main() {

   bool prime;
   int i;
   int n;

   i = 2   **   67;         // where to start checking divisors
   n = 1234567;   // number checking to see if prime

   prime = true;

   while (prime && i < n/2.0**67) {
      if (n % i == 0)    // is n divisible by i?
         prime = false;

      i = i + 1;

      ;
   }

   print(i-1);

}

