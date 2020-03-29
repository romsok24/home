use Net::POP3;
use IO::Socket::SSL;
    
$pop3host="smtp.gmail.com:587";
$musername="******kam1\@gmail.com";
$mpassword="******";


  my $socket = IO::Socket::SSL->new( PeerAddr => $pop3host,
                                     PeerPort => 587,
                                     Proto    => 'tcp') || die "No socket!";
  my $pop = Mail::POP3Client->new();
  $pop->User($musername);
  $pop->Pass($mpassword);
  $pop->Socket($socket);
  $pop->Connect();


  for( $i = 1; $i <= $pop->Count(); $i++ ) {
    foreach( $pop->Head( $i ) ) {
      /^(From|Subject):\s+/i && print $_, "\n";
    }
  }
  $pop->Close();

