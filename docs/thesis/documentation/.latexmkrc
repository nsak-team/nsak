##
## GLO -> GLS conversion hook (glossaries / glossaries-extra)
## Without this, latexmk never runs makeglossaries and \printglossary stays empty.
##
add_cus_dep( 'acn', 'acr', 0, 'makeglossaries' );
add_cus_dep( 'glo', 'gls', 0, 'makeglossaries' );
add_cus_dep( 'slo', 'sls', 0, 'makeglossaries' );
$clean_ext .= " acn acr alg glo gls glg slo sls slg ist";
sub makeglossaries {
   my ($base_name, $path) = fileparse( $_[0] );
   pushd $path;
   my $return = system "makeglossaries", $base_name;
   popd;
   return $return;
}

##
## Shell-escape for *latex (required by minted and the svg/inkscape packages)
##
set_tex_cmds( '--shell-escape %O %S' );

##
## Build with lualatex and run bibtex (project does not support pdflatex)
##
$pdf_mode = 4;
$postscript_mode = $dvi_mode = 0;
$bibtex_use = 1;
