import numpy as np
import tensorflow as tf
from . import inference
from .utils import misc_utils as utils
from .utils import vocab_utils
import sys
from importlib import import_module



class Hparam(object):
  src             = "en"
  tgt             = "hi"
  train_prefix        = None
  dev_prefix          = None
  test_prefix         = None
  vocab_prefix        = None
  out_dir           = None

     # Networks
  num_units           = 32
  num_layers          = 2
  dropout           = 0.2
  unit_type         = "lstm"
  encoder_type        = "uni"
  residual          = False
  time_major          = True
  num_embeddings_partitions   = 0

  # Attention mechanisms
  attention           = ""
  attention_architecture    = "standard"
  pass_hidden_state       = True

  # Train
  optimizer           = "sgd"
  num_train_steps       = 12000
  batch_size          = 128
  init_op           = "uniform"
  init_weight         = 0.1
  max_gradient_norm       = 5.0
  learning_rate         = 1.0
  learning_rate_warmup_steps  = 0
  learning_rate_warmup_factor = 1.0
  start_decay_step      = 0
  decay_factor        = 0.98
  decay_steps         = 10000
  learning_rate_decay_scheme  = ""
  colocate_gradients_with_ops = True

  # Data constraints
  num_buckets         = 5
  max_train           = 0
  src_max_len         = 50
  tgt_max_len         = 50
  source_reverse        = True

  # Inference
  src_max_len_infer       = None
  tgt_max_len_infer       = None
  infer_batch_size        = 32
  beam_width          = 0
  length_penalty_weight     = 0.0
  num_translations_per_input  = 1

  # Vocab
  sos             = "<s>"
  eos             = "</s>"
  bpe_delimiter         = None
  subword_option        = None
  check_special_token     = True
  num_residual_layers = None


  # Misc
  forget_bias         = 1.0
  num_gpus          = 1
  steps_per_stats       = 100
  steps_per_external_eval   = None
  share_vocab         = False
  metrics           = "bleu"
  log_device_placement    = False
  random_seed         = None
  override_loaded_hparams   = False
  scope             = None
  hparams_path        = None
  ckpt            = ""
  inference_input_file    = None
  inference_list        = None
  inference_output_file     = None
  inference_ref_file      = None
  jobid             = 0
  num_workers         = 1

FLAGS = None



def create_hparams(flags):
  """Create training hparams."""
  return tf.contrib.training.HParams(
      # Data
      src=flags.src,
      tgt=flags.tgt,
      train_prefix=flags.train_prefix,
      dev_prefix=flags.dev_prefix,
      test_prefix=flags.test_prefix,
      vocab_prefix=flags.vocab_prefix,
      out_dir=flags.out_dir,

      # Networks
      num_units=flags.num_units,
      num_layers=flags.num_layers,
      dropout=flags.dropout,
      unit_type=flags.unit_type,
      encoder_type=flags.encoder_type,
      residual=flags.residual,
      time_major=flags.time_major,
      num_embeddings_partitions=flags.num_embeddings_partitions,

      # Attention mechanisms
      attention=flags.attention,
      attention_architecture=flags.attention_architecture,
      pass_hidden_state=flags.pass_hidden_state,

      # Train
      optimizer=flags.optimizer,
      num_train_steps=flags.num_train_steps,
      batch_size=flags.batch_size,
      init_op=flags.init_op,
      init_weight=flags.init_weight,
      max_gradient_norm=flags.max_gradient_norm,
      learning_rate=flags.learning_rate,
      learning_rate_warmup_steps = flags.learning_rate_warmup_steps,
      learning_rate_warmup_factor = flags.learning_rate_warmup_factor,
      start_decay_step=flags.start_decay_step,
      decay_factor=flags.decay_factor,
      decay_steps=flags.decay_steps,
      learning_rate_decay_scheme=flags.learning_rate_decay_scheme,
      colocate_gradients_with_ops=flags.colocate_gradients_with_ops,

      # Data constraints
      num_buckets=flags.num_buckets,
      max_train=flags.max_train,
      src_max_len=flags.src_max_len,
      tgt_max_len=flags.tgt_max_len,
      source_reverse=flags.source_reverse,

      # Inference
      src_max_len_infer=flags.src_max_len_infer,
      tgt_max_len_infer=flags.tgt_max_len_infer,
      infer_batch_size=flags.infer_batch_size,
      beam_width=flags.beam_width,
      length_penalty_weight=flags.length_penalty_weight,
      num_translations_per_input=flags.num_translations_per_input,

      # Vocab
      sos=flags.sos if flags.sos else vocab_utils.SOS,
      eos=flags.eos if flags.eos else vocab_utils.EOS,
      bpe_delimiter=flags.bpe_delimiter,
      subword_option=flags.subword_option,
      check_special_token=flags.check_special_token,

      # Misc
      forget_bias=flags.forget_bias,
      num_gpus=flags.num_gpus,
      epoch_step=0,  # record where we were within an epoch.
      steps_per_stats=flags.steps_per_stats,
      steps_per_external_eval=flags.steps_per_external_eval,
      share_vocab=flags.share_vocab,
      metrics=flags.metrics.split(","),
      log_device_placement=flags.log_device_placement,
      random_seed=flags.random_seed,
      override_loaded_hparams=flags.override_loaded_hparams,
  )


def extend_hparams(hparams):
  """Extend training hparams."""
  # Sanity checks
  if hparams.encoder_type == "bi" and hparams.num_layers % 2 != 0:
    raise ValueError("For bi, num_layers %d should be even" %
                     hparams.num_layers)
  if (hparams.attention_architecture in ["gnmt"] and
      hparams.num_layers < 2):
    raise ValueError("For gnmt attention architecture, "
                     "num_layers %d should be >= 2" % hparams.num_layers)

  if hparams.subword_option and hparams.subword_option not in ["spm", "bpe"]:
    raise ValueError("subword option must be either spm, or bpe")
  if hparams.bpe_delimiter and hparams.bpe_delimiter != "@@":
    raise ValueError("BPE delimiter value must be '@@' %s",
                     hparams.bpe_delimiter)
  if hparams.bpe_delimiter == "@@":
    # if bpe_delimiter is set, subword_option will automatically set to bpe
    if hparams.subword_option == "spm":
      raise ValueError("Unable to set the subword option to spm "
                       "if bpe delimiter is set")
    else:
      hparams.subword_option = "bpe"

  # Flags
  utils.print_out("# hparams:")
  utils.print_out("  src=%s" % hparams.src)
  utils.print_out("  tgt=%s" % hparams.tgt)
  utils.print_out("  train_prefix=%s" % hparams.train_prefix)
  utils.print_out("  dev_prefix=%s" % hparams.dev_prefix)
  utils.print_out("  test_prefix=%s" % hparams.test_prefix)
  utils.print_out("  out_dir=%s" % hparams.out_dir)

  # Set num_residual_layers
  if hparams.residual and hparams.num_layers > 1:
    if hparams.encoder_type == "gnmt":
      # The first unidirectional layer (after the bi-directional layer) in
      # the GNMT encoder can't have residual connection due to the input is
      # the concatenation of fw_cell and bw_cell's outputs.
      num_residual_layers = hparams.num_layers - 2
    else:
      num_residual_layers = hparams.num_layers - 1
  else:
    num_residual_layers = 0
    utils.print_out("  Setting num_residual_layers =%d" % hparams.num_residual_layers)

  hparams.add_hparam("num_residual_layers", num_residual_layers)

  ## Vocab
  # Get vocab file names first
  if hparams.vocab_prefix:
    src_vocab_file = hparams.vocab_prefix + "." + hparams.src
    tgt_vocab_file = hparams.vocab_prefix + "." + hparams.tgt
  else:
    raise ValueError("hparams.vocab_prefix must be provided.")

  # Source vocab
  src_vocab_size, src_vocab_file = vocab_utils.check_vocab(
      src_vocab_file,
      hparams.out_dir,
      check_special_token=hparams.check_special_token,
      sos=hparams.sos,
      eos=hparams.eos,
      unk=vocab_utils.UNK)

  # Target vocab
  if hparams.share_vocab:
    utils.print_out("  using source vocab for target")
    tgt_vocab_file = src_vocab_file
    tgt_vocab_size = src_vocab_size
  else:
    tgt_vocab_size, tgt_vocab_file = vocab_utils.check_vocab(
        tgt_vocab_file,
        hparams.out_dir,
        check_special_token=hparams.check_special_token,
        sos=hparams.sos,
        eos=hparams.eos,
        unk=vocab_utils.UNK)
  hparams.add_hparam("src_vocab_size", src_vocab_size)
  hparams.add_hparam("tgt_vocab_size", tgt_vocab_size)
  hparams.add_hparam("src_vocab_file", src_vocab_file)
  hparams.add_hparam("tgt_vocab_file", tgt_vocab_file)

  # Check out_dir
  if not tf.gfile.Exists(hparams.out_dir):
    utils.print_out("# Creating output directory %s ..." % hparams.out_dir)
    tf.gfile.MakeDirs(hparams.out_dir)

  # Evaluation
  # for metric in hparams.metrics:
    hparams.add_hparam("best_" + metric, 0)  # larger is better
    best_metric_dir = os.path.join(hparams.out_dir, "best_" + metric)
    hparams.add_hparam("best_" + metric + "_dir", best_metric_dir)
    tf.gfile.MakeDirs(best_metric_dir)

  return hparams


def ensure_compatible_hparams(hparams, default_hparams, hparams_path):
  """Make sure the loaded hparams is compatible with new changes."""
  default_hparams = utils.maybe_parse_standard_hparams(
      default_hparams, hparams_path)

  # For compatible reason, if there are new fields in default_hparams,
  #   we add them to the current hparams
  default_config = default_hparams.values()
  config = hparams.values()
  for key in default_config:
    if key not in config:
      hparams.add_hparam(key, default_config[key])

  # Update all hparams' keys if override_loaded_hparams=True
  if default_hparams.override_loaded_hparams:
    for key in default_config:
      if getattr(hparams, key) != default_config[key]:
        utils.print_out("# Updating hparams.%s: %s -> %s" %
                        (key, str(getattr(hparams, key)),
                         str(default_config[key])))
        setattr(hparams, key, default_config[key])
  return hparams


def create_or_load_hparams(
    out_dir, default_hparams, hparams_path, save_hparams=True):
  """Create hparams or load hparams from out_dir."""
  hparams = utils.load_hparams(out_dir)
  if not hparams:
    hparams = default_hparams
    hparams = utils.maybe_parse_standard_hparams(
        hparams, hparams_path)
    hparams = extend_hparams(hparams)
  else:
    # hparams = extend_hparams(hparams)
    hparams = ensure_compatible_hparams(hparams, default_hparams, hparams_path)

  # Save HParams
  if save_hparams:
    utils.save_hparams(out_dir, hparams)
    for metric in hparams.metrics:
      utils.save_hparams(getattr(hparams, "best_" + metric + "_dir"), hparams)

  # Print HParams
  utils.print_hparams(hparams)
  return hparams


def run_main(flags,queue, default_hparams, inference_fn, target_session=""):
  """Run main."""
  # Job
  jobid = flags.jobid
  num_workers = flags.num_workers
  utils.print_out("# Job id %d" % jobid)

  # Random
  random_seed = flags.random_seed
  if random_seed is not None and random_seed > 0:
    utils.print_out("# Set random seed to %d" % random_seed)
    random.seed(random_seed + jobid)
    np.random.seed(random_seed + jobid)

  ## Train / Decode
  out_dir = flags.out_dir
  if not tf.io.gfile.exists(out_dir): tf.io.gfile.MakeDirs(out_dir)

  # Load hparams.
  hparams = create_or_load_hparams(
    out_dir, default_hparams, flags.hparams_path, save_hparams=(jobid==0))

  hparams.inference_indices = None
  
  # Inference
  ckpt = flags.ckpt
  if not ckpt:
    ckpt = tf.train.latest_checkpoint(out_dir)
  return inference_fn(ckpt, queue, hparams)

def start_nmt_thread(queue):
  global FLAGS
  FLAGS = Hparam()
  settings = import_module('demo.settings')
  FLAGS.out_dir = settings.BASE_DIR + '/translator/backend/resources/nmt_model'
  # FLAGS.hparams_path = '/home/abhishek/nmt-master/standard_hparams/wmt16_gnmt_8_layer.json'
  tf.compat.v1.app.run(main=main, argv=[queue])


def main(args):
  global FLAGS
  
  default_hparams = create_hparams(FLAGS)
  inference_fn = inference.quick_inference
  run_main(FLAGS, args[0], default_hparams, inference_fn)

# if __name__ == '__main__':
#     FLAGS = Hparam()
#     FLAGS.out_dir = '/home/abhishek/nmt-model'
#     FLAGS.hparams_path = '/home/abhishek/nmt-master/standard_hparams/wmt16_gnmt_8_layer.json'
#     tf.compat.v1.app.run(main=main, argv=[sys.argv[1]])
